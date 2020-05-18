import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import api from '../../services/api';

import HeaderApp from '../../components/HeaderApp'

import './styles.css'

export default function NewAttendance() {
    const [userid, setUserid] = useState('');
    const [name, setName] = useState('');
    const [gender, setGender] = useState('');
    const [age, setAge] = useState(0);
    const [height, setHeight] = useState(0);
    const [weight, setWeight] = useState(0);
    const [temperature, setTemperature] = useState(0);
    const [readOnly, setReadOnly] = useState(false);

    const [influenza, setInfluenza] = useState('DESCONHECIDO');
    const [parainfluenza, setParainfluenza] = useState('DESCONHECIDO');
    const [h1n1, setH1n1] = useState('DESCONHECIDO');
    const [chlamydophila, setChlamydophila] = useState('DESCONHECIDO');
    const [rhinovirus, setRhinovirus] = useState('DESCONHECIDO');
    const [virussincicial, setVirussincicial] = useState('DESCONHECIDO');
    const [outroscov, setOutroscov] = useState('DESCONHECIDO');
    const [outrasinfeccoes, setOutrasinfeccoes] = useState('DESCONHECIDO');

    const [hemacias, setHemacias] = useState(0);
    const [hematocrito, setHematocrito] = useState(0);
    const [hemoglobinas, setHemoglobinas] = useState(0);
    const [vcm, setVcm] = useState(0);
    const [hcm, setHcm] = useState(0);
    const [chcm, setChcm] = useState(0);
    const [rdw, setRdw] = useState(0);
    const [eritoblastos, setEritoblastos] = useState(0);

    const [leucocitos, setLeucocitos] = useState(0);
    const [mielocitos, setMielocitos] = useState(0);
    const [metamielocitos, setMetamielocitos] = useState(0);
    const [bastonetes, setBastonetes] = useState(0);
    const [segmentados, setSegmentados] = useState(0);
    const [neutrofilos, setNeutrofilos] = useState(0);
    const [eosinofilos, setEosinofilos] = useState(0);
    const [basofilos, setBasofilos] = useState(0);
    const [linfocitos, setLinfocitos] = useState(0);
    const [monocitos, setMonocitos] = useState(0);
    const [plasmocitos, setPlasmocitos] = useState(0);
    const [pcr, setPcr] = useState(0);

    const [plaquetas, setPlaquetas] = useState(0);
    const [vmp, setVmp] = useState(0);


    const token = localStorage.getItem('token');
    const history = useHistory();

    

    function handleUserClear(e) {
        e.preventDefault();
        setUserid('');
        setName('');
        setGender('');
        setReadOnly(false);
    }

    async function handleSubmit(e) {
        e.preventDefault();
        const data = {
            userid: userid,
            name: name,
            gender: gender,
            age: age,
            height: height,
            weight: weight,
            temperature: temperature,
            influenza: influenza,
            parainfluenza: parainfluenza,
            h1n1: h1n1,
            chlamydophila: chlamydophila,
            rhinovirus: rhinovirus,
            virussincicial: virussincicial,
            outroscov: outroscov,
            outrasinfeccoes, outrasinfeccoes,
            hemacias: hemacias,
            hematocrito: hematocrito,
            hemoglobinas: hemoglobinas,
            vcm: vcm,
            hcm: hcm,
            chcm: chcm,
            rdw: rdw,
            eritoblastos: eritoblastos,
            leucocitos: leucocitos,
            mielocitos: mielocitos,
            metamielocitos: metamielocitos,
            bastonetes: bastonetes,
            segmentados: segmentados,
            neutrofilos: neutrofilos,
            eosinofilos: eosinofilos,
            basofilos: basofilos,
            linfocitos: linfocitos,
            monocitos: monocitos,
            plasmocitos: plasmocitos,
            pcr: pcr,
            plaquetas: plaquetas,
            vmp: vmp
        }
        console.log(data);

        const headers = {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        };

        try {
            await api.post('attendances', data, headers);
            history.push('/dashboard');
        } catch(error) {
            console.log(error);
        }
        
    }

    async function handleSearchUser(e) {
        e.preventDefault();

        const headers = {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        };

        try {
            const response = await api.get(`users?userid=${userid}`, headers);
            const users = response.data.items;
            if (users.length === 1) {
                const user = users[0];
                setName(user.name);
                setGender(user.gender);
                setReadOnly(true);
            } else {
                alert("Paciente nao encontrado.");
            }
        } catch (error) {
            alert(error);
        }
    }
    return (
        <div>
            <HeaderApp />
            <div className="new-attendance-box">
                
                <h1>NOVO ATENDIMENTO</h1>
                <h2>IDENTIFICAÇÃO DO PACIENTE</h2>
                <p>
                    SE O PACIENTE JÁ ESTIVER CADASTRADO NO SISTEMA, AO CLICAR EM BUSCAR O SISTEMA ATRIBUIRÁ
                    ESTA CONSULTA A ELE. CASO ELE AINDA NÃO SEJA CADASTRADO, BASTA
                    SEGUIR NORMALMENTE QUE ELE SERÁ CADASTRADO AUTOMATICAMENTE.
                </p>
                <div className="new-attendance-item">
                    <div className="label-float">
                        <input form="submitForm"
                            placeholder=" "
                            required
                            value={userid}
                            onChange={e => setUserid(e.target.value)}
                            readOnly={readOnly}
                        />
                        <label>ID DO PACIENTE</label>
                    </div>

                    <button className="button" onClick={handleSearchUser}>BUSCAR</button>
                    <button className="button" onClick={handleUserClear}>LIMPAR</button>
                </div>

                <h2>INFORMAÇÕES GERAIS</h2>

                <div className="new-attendance-item">
                    <div className="label-float">
                        <input form="submitForm"
                            placeholder=" "
                            required
                            value={name}
                            onChange={e => setName(e.target.value)}
                            readOnly={readOnly}
                        />
                        <label>NOME</label>
                    </div>
                    <div className="label-float">
                        <select form="submitForm"
                            onChange={e => setGender(e.target.value)}>
                            <option value="indefinido">Indefinido</option>
                            <option value="masculino">Masculino</option>
                            <option value="feminino">Feminino</option>
                        </select>
                        <label>GÊNERO</label>
                    </div>
                    <div className="label-float">
                        <input form="submitForm"
                            type="number"
                            required
                            min="0"
                            max="130"
                            step="1"
                            value={age}
                            onChange={e => setAge(e.target.value)}
                            placeholder=" "
                        />
                        <label>IDADE (anos)</label>
                    </div>
                    <div className="label-float">
                        <input form="submitForm"
                            type="number"
                            min="0"
                            max="250"
                            step="0.1"
                            value={height}
                            onChange={e => setHeight(e.target.value)}
                            placeholder=" "
                            required
                        />
                        <label>ALTURA (cm)</label>
                    </div>
                    <div className="label-float">
                        <input form="submitForm"
                            type="number"
                            min="0"
                            max="300"
                            step="0.1"
                            value={weight}
                            onChange={e => setWeight(e.target.value)}
                            placeholder=" "
                            required
                        />
                        <label>PESO (Kg)</label>
                    </div>
                    <div className="label-float">
                        <input form="submitForm"
                            type="number"
                            min="0"
                            max="50"
                            step="0.1"
                            value={temperature}
                            onChange={e => setTemperature(e.target.value)}
                            placeholder=" "
                            required
                        />
                        <label>TEMPERATURA (°C)</label>
                    </div>
                </div>

                <h2>PRESENÇA DE OUTRAS DOENÇAS</h2>
                <p>
                    ESTA PARTE DO FORMULÁRIO É OPCIONAL. ELA NÃO É REQUERIDA PARA A ANÁLISE SER FEITA,
                    ENTRETANTO, O FORNECIMENTO DESTAS INFORMAÇÕES (QUANDO DISPONÍVEIS) PODEM AUMENTAR
                    SIGNIFICATIVAMENTE A PRECISÃO DAS ANÁLISES.
                </p>
                <div className="new-attendance-item">
                    <div className="radio-float">
                        <label class="radio-name">INFLUENZA</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="influenza"
                                value="DESCONHECIDO"
                                onChange={e => setInfluenza(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="influenza"
                                value="SIM"
                                onChange={e => setInfluenza(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="influenza"
                                value="NÃO"
                                onChange={e => setInfluenza(e.target.value)}
                            />
                            NÃO
                        </label>
                        
                    </div>
                    <div className="radio-float">
                        <label class="radio-name">PARAINFLUENZA</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="parainfluenza"
                                value="DESCONHECIDO"
                                onChange={e => setParainfluenza(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="parainfluenza"
                                value="SIM"
                                onChange={e => setParainfluenza(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="parainfluenza"
                                value="NÃO"
                                onChange={e => setParainfluenza(e.target.value)}
                            />
                            NÃO
                        </label>
                    </div>
                    
                    <div className="radio-float">
                        <label class="radio-name">H1N1</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="h1n1"
                                value="DESCONHECIDO"
                                onChange={e => setH1n1(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="h1n1"
                                value="SIM"
                                onChange={e => setH1n1(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="h1n1"
                                value="NÃO"
                                onChange={e => setH1n1(e.target.value)}
                            />
                            NÃO
                        </label>
                    </div>
                    <div className="radio-float">
                        <label class="radio-name">CHLAMYDOPHILA PNEUMONIAE</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="chlamydophila"
                                value="DESCONHECIDO"
                                onChange={e => setChlamydophila(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="chlamydophila"
                                value="SIM"
                                onChange={e => setChlamydophila(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="chlamydophila"
                                value="NÃO"
                                onChange={e => setChlamydophila(e.target.value)}
                            />
                            NÃO
                        </label>
                    </div>

                    <div className="radio-float">
                        <label class="radio-name">RHINOVIRUS/ENTEROVIRUS</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="rhinovirus"
                                value="DESCONHECIDO"
                                onChange={e => setRhinovirus(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="rhinovirus"
                                value="SIM"
                                onChange={e => setRhinovirus(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="rhinovirus"
                                value="NÃO"
                                onChange={e => setRhinovirus(e.target.value)}
                            />
                            NÃO
                        </label>
                    </div>
                    
                    <div className="radio-float">
                        <label class="radio-name">VÍRUS SINCICIAL RESPIRATÓRIO</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="virussincicial"
                                value="DESCONHECIDO"
                                onChange={e => setVirussincicial(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="virussincicial"
                                value="SIM"
                                onChange={e => setVirussincicial(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="virussincicial"
                                value="NÃO"
                                onChange={e => setVirussincicial(e.target.value)}
                            />
                            NÃO
                        </label>
                    </div>

                    <div className="radio-float">
                        <label class="radio-name">OUTROS CORONAVÍRUS</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="outroscov"
                                value="DESCONHECIDO"
                                onChange={e => setOutroscov(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="outroscov"
                                value="SIM"
                                onChange={e => setOutroscov(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="outroscov"
                                value="NÃO"
                                onChange={e => setOutroscov(e.target.value)}
                            />
                            NÃO
                        </label>
                    </div>

                    <div className="radio-float">
                        <label class="radio-name">OUTRAS INFECÇÕES RESPIRATÓRIAS</label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="outrasinfeccoes"
                                value="DESCONHECIDO"
                                onChange={e => setOutrasinfeccoes(e.target.value)}
                            />
                            DESCONHECIDO
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="outrasinfeccoes"
                                value="SIM"
                                onChange={e => setOutrasinfeccoes(e.target.value)}
                            />
                            SIM
                        </label>
                        <label>
                            <input form="submitForm"
                                type="radio"
                                name="outrasinfeccoes"
                                value="NÃO"
                                onChange={e => setOutrasinfeccoes(e.target.value)}
                            />
                            NÃO
                        </label>
                    </div>

                </div>
                <h2>HEMOGRAMA</h2>
                <div>
                    <h2>ERITOGRAMA</h2>
                    <div className="new-attendance-item">

                        <div className="label-float">
                            <input form="submitForm"
                                value={hemacias}
                                required
                                onChange={e => setHemacias(e.target.value)}
                                placeholder=" "
                            />
                            <label>HEMÁCIAS (tera/L)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={hematocrito}
                                required
                                onChange={e => setHematocrito(e.target.value)}
                                placeholder=" "
                            />
                            <label>HEMATÓCRITO (%)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={hemoglobinas}
                                required
                                onChange={e => setHemoglobinas(e.target.value)}
                                placeholder=" "
                            />
                            <label>HEMOGLOBINAS (g/dL)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={vcm}
                                onChange={e => setVcm(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>VCM (fL)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={hcm}
                                onChange={e => setHcm(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>HCM (pg)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={chcm}
                                onChange={e => setChcm(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>CHCM (g/dL)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={rdw}
                                onChange={e => setRdw(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>RDW (%)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={eritoblastos}
                                onChange={e => setEritoblastos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>ERITOBLASTOS (/100 leuco)</label>
                        </div>

                    </div>
                    <h2>LEUCOGRAMA + PCR</h2>
                    <div className="new-attendance-item">

                        <div className="label-float">
                            <input form="submitForm"
                                value={leucocitos}
                                onChange={e => setLeucocitos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>LEUCÓCITOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={mielocitos}
                                onChange={e => setMielocitos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>MIELÓCITOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={metamielocitos}
                                onChange={e => setMetamielocitos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>METAMIELÓCITOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={bastonetes}
                                onChange={e => setBastonetes(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>BASTONETES (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={segmentados}
                                onChange={e => setSegmentados(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>SEGMENTADOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={neutrofilos}
                                onChange={e => setNeutrofilos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>NEUTRÓFILOS TOTAIS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={eosinofilos}
                                onChange={e => setEosinofilos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>EOSINÓFILOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={basofilos}
                                onChange={e => setBasofilos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>BASÓFILOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={linfocitos}
                                onChange={e => setLinfocitos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>LINFÓCITOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={monocitos}
                                onChange={e => setMonocitos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>MONÓCITOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={plasmocitos}
                                onChange={e => setPlasmocitos(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>PLASMÓCITOS (/mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={pcr}
                                onChange={e => setPcr(e.target.value)}
                                placeholder=" "
                                required
                            />
                            <label>PCR (mg/L)</label>
                        </div>

                    </div>

                    <h2>PLAQUETOGRAMA</h2>
                    <div className="new-attendance-item">

                        <div className="label-float">
                            <input form="submitForm"
                                value={plaquetas}
                                onChange={e => setPlaquetas(e.target.value)}
                                placeholder=" "
                            />
                            <label>PLAQUETAS (/103 mm3)</label>
                        </div>
                        <div className="label-float">
                            <input form="submitForm"
                                value={vmp}
                                onChange={e => setVmp(e.target.value)}
                                placeholder=" "
                            />
                            <label>VMP (fL)</label>
                        </div>

                    </div>

                </div>
                <form id="submitForm" onSubmit={(e) => handleSubmit(e)}>
                    <input className="button-full-width" type="submit" value="ANALISAR" >

                    </input>
                </form>

            </div>
        </div>
    )
}