import axios from 'axios';

const api = axios.create({
   baseURL: 'http://3.22.176.142:5000/api/' 
});

export default api;