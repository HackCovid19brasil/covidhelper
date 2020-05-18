import pandas as pd
import numpy as np
from scipy import linalg
from prince import PCA
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from shap import waterfall_plot, TreeExplainer
import joblib 

class labtest_predictor:
    """
        To be commented    
    """
    #Class variables
    model_variables = ['Idade', 'Plaquetas', 'VMP', 'Hemácias', 'Linfócitos', 'CHCM', 'Leucócitos', 
                        'Basófilos', 'Eosinófilos', 'VCM', 'Monócitos', 'RDW', 'Outra gripe']
    norm = {'rdw': {'avg': 13.6043, 'std':0.850362},
            'vmp': {'avg': 9.95539, 'std':1.01304},
            'vcm': {'avg': 91.0455, 'std':4.64755},
            'chcm': {'avg': 32.5655, 'std':1.02971},
            'hemacias': {'avg': 4.79364, 'std':0.416998},
            'plaquetas': {'avg': 227061, 'std':2474.57},
            'linfocitos': {'avg': 2124.92, 'std':685.689},
            'basofilos': {'avg': 31.8886, 'std':18.0486},
            'leucocitos': {'avg': 6440.36, 'std':1711.63},
            'eosinofilos': {'avg': 245.356, 'std':194.075},
            'monocitos': {'avg': 359.505, 'std':174.026} }
    
    probs_df = pd.read_csv('app/ai_models/plot_files/plot_1_probs.csv') # Plot 1
    
    train_df = pd.read_csv('app/ai_models/plot_files/plot_3_4_train_df.csv') # Plot 3

    classifier = joblib.load('app/ai_models/classificador_lucas.pkl') #load only once

    #End of class variables

    def __init__(self, patient_dict):
        self.patient_dict = patient_dict    

    def preprocessing(self):
        #Data normalization (accordclearing to brazilian population)
        
        idade_quantile = int(np.floor(self.patient_dict['age']/5))
        rdw_norm = self.normalizer(float(self.patient_dict['cbc']['rdw']),self.norm, 'rdw')
        vmp_norm = self.normalizer(float(self.patient_dict['cbc']['vmp']),self.norm, 'vmp')
        plaquetas_norm = self.normalizer(float(self.patient_dict['cbc']['plaquetas']),self.norm, 'plaquetas')
        chcm_norm = self.normalizer(float(self.patient_dict['cbc']['chcm']),self.norm, 'chcm')
        vcm_norm = self.normalizer(float(self.patient_dict['cbc']['vcm']),self.norm, 'vcm')
        hemacias_norm = self.normalizer(float(self.patient_dict['cbc']['hemacias']),self.norm, 'hemacias')
        linfocitos_norm = self.normalizer(float(self.patient_dict['cbc']['linfocitos']),self.norm, 'linfocitos')
        basofilos_norm = self.normalizer(float(self.patient_dict['cbc']['basofilos']),self.norm, 'basofilos')
        leucocitos_norm = self.normalizer(float(self.patient_dict['cbc']['leucocitos']),self.norm, 'leucocitos')
        eosinofilos_norm = self.normalizer(float(self.patient_dict['cbc']['eosinofilos']),self.norm, 'eosinofilos')
        monocitos_norm = self.normalizer(float(self.patient_dict['cbc']['monocitos']),self.norm, 'monocitos')

        #Is the patient diagnosed with any respiratory infection? (has_disease)
        has_disease = int(any([result==1 for result in self.patient_dict['respiratory_infections'].values()]))

        patient_preprocessed = {
            'Idade': idade_quantile,
            'Plaquetas': plaquetas_norm,
            'VMP': vmp_norm,
            'Hemácias': hemacias_norm,
            'Linfócitos': linfocitos_norm,
            'CHCM': chcm_norm,
            'Leucócitos': leucocitos_norm,
            'Basófilos': basofilos_norm,
            'Eosinófilos': eosinofilos_norm,
            'VCM': vcm_norm,
            'Monócitos': monocitos_norm,
            'RDW': rdw_norm,
            'Outra gripe': has_disease
        }
        return patient_preprocessed

    def predict(self, patient_preprocessed):
        patient_vars_model = []
        for var in self.model_variables:
            patient_vars_model.append(patient_preprocessed[var])
            
        pred = self.classifier.predict_proba(np.array([patient_vars_model]))[0]
        pred_class = int(np.argmax(pred))
        pred_proba = float(np.max(pred))
        return {'pred_class': pred_class, 'pred_proba': pred_proba}

    def model_interpretation(self, patient_id, patient_preprocessed, pred, prob, model):
        '''
        Fazer gráficos avaliativos do modelo.
        Argumentos:
            patient_id = string referente a identificação do paciente
            patient_preprocessed = dicionario contendo dados do exame do paciente
            pred = classe predita pelo modelo
            prob = probabilidade referente a classe predita pelo modelo
            model = objeto do modelo
        '''
        #### Pegar variaveis necessárias para o plot (import csv)
        
        #### Nome dos plots
        
        plot_1_name = 'app/ai_models/temp/probacurve-'+str(patient_id)+'.png'
        plot_2_name = 'app/ai_models/temp/shap-'+str(patient_id)+'.png'
        plot_3_name = 'app/ai_models/temp/dist-'+str(patient_id)+'.png'
        plot_4_name = 'app/ai_models/temp/mapa-'+str(patient_id)+'.png'


        #URL API PLOTS
        plot_1_api = "http://localhost:5000/api/media/probacurve-"+str(patient_id)+".png"
        plot_2_api = "http://localhost:5000/api/media/shap-"+str(patient_id)+".png"
        plot_3_api = "http://localhost:5000/api/media/dist-"+str(patient_id)+".png"
        plot_4_api = "http://localhost:5000/api/media/mapa-"+str(patient_id)+".png"
        
        #### Configurações gerais do plt
        DPI_IMAGES=100
        FONT_SIZE = 8
        FONT_NAME = 'sans-serif'
        plt.rc('font',family=FONT_NAME, size=FONT_SIZE)
        plt.rc('axes', titlesize=FONT_SIZE, labelsize=FONT_SIZE)
        plt.rc('xtick', labelsize=FONT_SIZE)
        plt.rc('ytick', labelsize=FONT_SIZE)
        plt.rc('legend', fontsize=FONT_SIZE)
        
        #### PLOT 1 - Distribuição da probabilidade dada pelo modelo para pacientes positivos
        # Itens Necessário: self.probs_df(csv importado) e pred
        exame_resp = pred
        exame_prob = prob
        # Plot
        fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
        sns.kdeplot(self.probs_df['prob_neg'], shade=True, color='#386796', ax=axis, linestyle="--", label='Casos Negativos')
        sns.kdeplot(self.probs_df['prob_pos'], shade=True, color='#F06C61', ax=axis, label='Casos positivos')
        # Pegar eixo XY do Plt object para fazer a interpolação
        if exame_resp == 0:
            xi = 1 - exame_prob
            data_x, data_y = axis.lines[0].get_data()
        elif exame_resp == 1:
            xi = exame_prob
            data_x, data_y = axis.lines[1].get_data()
        # Fazer a interpolação e plot
        yi = np.interp(xi, data_x, data_y)
        axis.plot([xi],[yi], linestyle = 'None', marker="*", color='black', markersize=10, label='Paciente')
        # Outras configuracoes do plot
        axis.legend(loc="upper right")
        #axis.set_title('Probabilidade de ser COVID Positivo pelo modelo', fontweight='bold')
        axis.set_xlim([0, 1])
        axis.set_ylim([0, axis.get_ylim()[1]])
        plt.tight_layout()
        # Salvar plot 1
        plt.savefig(plot_1_name, dpi=DPI_IMAGES, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        
        #### PLOT 2 - SHAP
        # Necessário: patient_preprocessed, pred e model
        features = np.array(list(patient_preprocessed.keys()))
        sample_x = np.array(list(patient_preprocessed.values()))
        # Calcular SHAP Value  
        explainer = TreeExplainer(model=model)                # Faz o objeto SHAP
        shap_values_sample = explainer.shap_values(sample_x)  # Calculo do SHAP
        expected_value = explainer.expected_value[exame_resp] # Pega o baseline para a classe predita pelo modelo
        shap_values_sample = explainer.shap_values(sample_x)  # Calcular os SHAP values
        # Plot
        #plt.title('Valores SHAP', fontweight='bold')
        waterfall_plot(expected_value, shap_values_sample[exame_resp], sample_x, feature_names=features, max_display=20, show=False)
        # Salvar imagem
        plt.tight_layout()
        plt.savefig(plot_2_name, dpi=DPI_IMAGES, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        #### PLOT 3 - Distribuição das variáveis mais importantes para o modelo
        # Necessário: self.train_df(csv importado), patient_preprocessed, pred
        important_features = ['Leucócitos', 'Plaquetas', 'Hemácias', 'Eosinófilos']
        target_0 = self.train_df[self.train_df['target'] == 0][['Leucócitos', 'Plaquetas', 'Hemácias', 'Eosinófilos']]
        target_1 = self.train_df[self.train_df['target'] == 1][['Leucócitos', 'Plaquetas', 'Hemácias', 'Eosinófilos']]
        # Plot
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,5))
        # Plot settings
        #sns.set_color_codes()
        #st = fig.suptitle("Distribuição das variáveis importantes para o modelo", fontweight='bold')
        #st.set_y (1.05)
        # Index col/row
        r = 0
        c = 0
        # Loop to plot
        for feat in important_features:
            # Plot distribuição
            sns.kdeplot(list(target_0[feat]), shade=True, color='#386796', ax=axes[r][c], label='Casos Negativos', linestyle="--")
            sns.kdeplot(list(target_1[feat]), shade=True, color='#F06C61', ax=axes[r][c], label='Casos positivos')
            # Pegar a curva de densidade a partir do resultado do modelo
            if pred == 0:
                data_x, data_y = axes[r][c].lines[0].get_data()
            elif pred == 1:
                data_x, data_y = axes[r][c].lines[1].get_data()
            # Pegar a informação (valor) daquela variável importante
            xi = patient_preprocessed[feat]
            yi = np.interp(xi, data_x, data_y)
            ## Plot ponto na curva
            axes[r][c].plot([xi],[yi], linestyle = 'None', marker="*", color='black', markersize=10, label='Paciente')
            axes[r][c].set_title(feat)
            axes[r][c].legend(loc="upper right")
            axes[r][c].set_ylim([0, axes[r][c].get_ylim()[1]])
            # Mudar onde sera plotado
            if c == 0:
                c += 1
            else:
                r += 1
                c = 0
        # Ajeitar o plot
        plt.tight_layout()
        # Salvar imagem
        plt.savefig(plot_3_name, dpi=DPI_IMAGES, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        
        #### PLOT 4 - Mapa com SVD para os pacientes
        # Necessário: train_df(csv importado), patient_preprocessed
        amostra = pd.DataFrame(patient_preprocessed, index=[0,]).drop(axis=1, columns=['Outra gripe'])
        
        # Fazer PCA com SVD via prince package
        y_train = self.train_df['target']                                                 # Salvar coluna target
        dados = self.train_df.drop(axis=1, columns=['Outra gripe', 'target']).copy()      # Dataset para criar o mapa
        pca_obj = PCA(n_components=2, random_state=42)                               # Objeto do PCA   
        pca_obj.fit(dados)                                                           # Fit no conjunto de dados
        componentes = pca_obj.transform(dados)                                       # Criar os componentes principais dos dados
        transf = pca_obj.transform(amostra)                                          # Transformar paciente para PCA
        xi = transf.loc[0,0]                                                         # Eixo X do paciente para plot
        yi = transf.loc[0,1]                                                         # Eixo Y do paciente para plot
        comp = pd.DataFrame()                                                        # Dataframe para conter os componentes
        comp['C1'] = componentes[0]                                                  # Componente Principal 1
        comp['C2'] = componentes[1]                                                  # Componente Principal 2
        comp['TG'] = y_train                                                         # Variável target para a mascara
        comp_0 = comp[comp['TG'] == 0][['C1', 'C2']]                                 # Dataframe de CP para negativos
        comp_1 = comp[comp['TG'] == 1][['C1', 'C2']]                                 # Dataframe de CP para positivos
        # Plot
        fig, ax = plt.subplots(figsize=(8,8))
        plt.margins(0,0)
        sns.scatterplot(ax=ax, data=comp_0, x='C1',y='C2', color='#386796', label='Casos Negativos')
        sns.scatterplot(ax=ax, data=comp_1, x='C1',y='C2', color='#F06C61', label='Casos Positivos')
        x_mean, y_mean, width, height, angle = self.build_ellipse(comp_0['C1'], comp_0['C2'])
        ax.add_patch(Ellipse((x_mean, y_mean), width, height, angle=angle, linewidth=2, color='#386796', fill=True, alpha=0.2))
        x_mean, y_mean, width, height, angle = self.build_ellipse(comp_1['C1'], comp_1['C2'])
        ax.add_patch(Ellipse((x_mean, y_mean), width, height, angle=angle, linewidth=2, color='#F06C61', fill=True, alpha=0.2))
        ax.plot([xi],[yi], linestyle = 'None', marker="*", color='black', markersize=10, label='Paciente')
        # Configurações do plot
        #ax.set_title('Similaridade entre pacientes',fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylabel('')
        ax.set_xlabel('')
        handles, labels = ax.get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        ax.legend(handles, labels, loc="upper right")
        # Salvar imagem
        plt.axis('off')
        plt.savefig(plot_4_name, dpi=DPI_IMAGES, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        # Retornar
        model_result = {'prediction': pred,
                        'probability': str(round(prob*100, 2)),
                        'probacurve': plot_1_api,
                        'shap_img': plot_2_api,
                        'dist_img': plot_3_api,
                        'mapa_img': plot_4_api}
        return model_result


        """
        Helper functions go here
        """
    def normalizer(self, value, norm_dict, norm_key):
        return (value -  norm_dict[norm_key]['avg'])/norm_dict[norm_key]['std']

    def build_ellipse(self, X, Y):
            """Construct ellipse coordinates from two arrays of numbers.
            Args:
                X (1D array_like)
                Y (1D array_like)
            Returns:
                float: The mean of `X`.
                float: The mean of `Y`.
                float: The width of the ellipse.
                float: The height of the ellipse.
                float: The angle of orientation of the ellipse.
            """
            x_mean = np.mean(X)
            y_mean = np.mean(Y)

            cov_matrix = np.cov(np.vstack((X, Y)))
            U, s, V = linalg.svd(cov_matrix, full_matrices=False)

            chi_95 = np.sqrt(4.61)  # 90% quantile of the chi-square distribution
            width = np.sqrt(cov_matrix[0][0]) * chi_95 * 2
            height = np.sqrt(cov_matrix[1][1]) * chi_95 * 2

            eigenvector = V.T[0]
            angle = np.arctan(eigenvector[1] / eigenvector[0])

            return x_mean, y_mean, width, height, angle

    