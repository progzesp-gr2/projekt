import axios from 'axios';

const client = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});


client.interceptors.request.use((config) => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  if (match) config.headers['X-CSRFToken'] = match[1];
  return config;
});


export default client;