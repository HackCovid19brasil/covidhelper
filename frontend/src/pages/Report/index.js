import React, { useEffect, useState} from 'react';

import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import HelpRounded from '@material-ui/icons/HelpRounded';
import Popup from "reactjs-popup";
import './styles.css'

import HeaderApp from '../../components/HeaderApp'
import ResultBox from '../../components/ResultBox'
import api from '../../services/api';


export default function Report(props) {
    const id = props.location.state.detail.id;
    const token = localStorage.getItem('token');

    const [result, setResult] = useState('ANALISE');
    const [result_proba, setResultproba] = useState(' ');

    const [shapImg, setShap] = useState('https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif');
    const [mapaImg, setMapa] = useState('https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif');
    const [probaImg, setProba] = useState('https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif');
    const [distImg, setDist] = useState('https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif');
    
    useEffect(() => {
      // Create an scoped async function in the hook
      async function anyNameFunction() {
        const response = await api.get(`predict_labtest/${id}`, {
          headers: {
              'Authorization': `Bearer ${token}`
          }
      });

      setShap(response.data.shap_img);
      setMapa(response.data.mapa_img);
      setProba(response.data.probacurve);
      setDist(response.data.dist_img);
      setResult(response.data.prediction);
      setResultproba(response.data.probability);

      }    // Execute the created function directly
      anyNameFunction();
      
    }, []);

    const Tooltip = () => (
        <Popup
          trigger={open => (
            <IconButton aria-label="delete"><HelpRounded /></IconButton>
          )}
          position="right center"
          closeOnDocumentClick
        >
          <span>
            OBS.: Os valores de SHAP podem ser interpretados como "forças", onde cada valor de SHAP calculado para o exame é uma força que 
            aumenta/diminui a probabilidade de um paciente ser diagnosticado com SARS-CoV-2. Note que a interação de
             combinações de recursos pode ser descoberta usando este método.
          </span>
        </Popup>
    );

    const TooltipMapa = () => (
        <Popup
          trigger={open => (
            <IconButton aria-label="delete"><HelpRounded /></IconButton>
          )}
          position="right center"
          closeOnDocumentClick
        >
          <span>
            Perceba que pacientes infectados e saudáveis tem exames laboratórias 
            mais parecidos entre si. Este gráfico é calculado a partir da 
            Análise de Componentes Principais.
          </span>
        </Popup>
    );

    const TooltipProba = () => (
        <Popup
          trigger={open => (
            <IconButton aria-label="delete"><HelpRounded /></IconButton>
          )}
          position="right center"
          closeOnDocumentClick
        >
          <span>
            Este gráfico pode ser entendendido como uma distribuição 
            de pontuação para a infecção pelo vírus, ou seja, quanto mais para 
            a direita no eixo X (maior pontuação), maior a chance de a pessoa estar 
            contaminada. Dessa forma é possível visualizar se o paciente 
            está em alguma região de dúvida ou certeza do modelo.
          </span>
        </Popup>
    );

    const TooltipDist = () => (
        <Popup
          trigger={open => (
            <IconButton aria-label="delete"><HelpRounded /></IconButton>
          )}
          position="right center"
          closeOnDocumentClick
        >
          <span>
            É útil visualizar como um paciente se encontra em relação outros 
            diagnosticados em cada exame laboratorial. Porém o modelo toma 
            decisões considerando também a interação entre todas as 
            informações fornecidas.
          </span>
        </Popup>
    );

    
    return(
        


        <div>
            <HeaderApp/>
            <div className="report-box">
                <h1>Relatório de Previsão para SARS-CoV-2</h1>


                <ResultBox result={result} proba={result_proba}/>

                <div className="box-50">
                    <div className="report-item plot-box-50">
                        <div className="plot-header">
                            <h3>Como cada componente do exame contribuiu para o resultado:</h3>
                            <Tooltip/>
                        </div>
                        <div className="plot-figure"> 
                            <img src={shapImg} alt="Valores SHAP para previsão do status COVID do paciente"></img>
                        </div>
                        <div className="plot-explanation-text">
                            <ul>
                                <li>O eixo x indica a contribuição de cada variável na decisão do modelo. Este valor é chamado SHAP.</li>
                                <li>A cor vermelha indica que o exame contribuiu na direção do resultado final do modelo, e azul quando ele contribuiu para o resultado oposto.</li>
                            </ul>
                        </div>
                    </div>

                    <div className="report-item plot-box-50">
                        <div className="plot-header">
                            <h3>Similaridade entre pacientes</h3>
                            <TooltipMapa/>
                        </div>
                        <div className="plot-figure">
                            <img src={mapaImg} alt="Mapa de similaridade entre pacientes"></img>
                        </div>
                        <div className="plot-explanation-text">
                            <ul>
                                <li>Quanto menor a distância entre dois pontos, mais parecidos são os pacientes com respeito aos exames.</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="box-7030">
                    <div className="report-item plot-box-30">
                        <div className="plot-header">
                            <h3>Como o paciente está em relação a outros no diagnóstico para COVID</h3>
                            <TooltipProba/>
                        </div>
                        <div className="plot-figure">
                            <img src={probaImg} alt="Probabilidade do paciente estar com SARS-CoV-2 versus histórico do modelo em outros pacientes"></img>
                        </div>
                        <div className="plot-explanation-text">
                            <span>Este gráfico apresenta a função de probabilidade dos exames serem de um 
                                paciente com SARS-CoV-2. </span>
                        </div>
                    </div>

                    <div className="report-item plot-box-70">
                        <div className="plot-header">
                            <h3>Distribuição dos pacientes nos exames mais importantes</h3>
                            <TooltipDist/>
                        </div>
                        <div className="plot-figure">
                            <img src={distImg} alt="Curva densidade de probabilidade de valores para exames em pacientes com e sem covid"></img>
                        </div>
                        <div className="plot-explanation-text">
                            <span>Os gráficos mostram a distribuição dos exames mais importantes 
                                (segundo o modelo) para pacientes já testados. A estrela indica o 
                                paciente em relação aos demais.</span>
                        </div>
                    </div>
            </div>



            </div>

            

            
            
        </div>
    )
}