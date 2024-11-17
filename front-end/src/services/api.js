import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Flask backend URL
});

export const fetchUsers = () => API.get('/users');
export const addUser = (user) => API.post('/users', user);

export const fetchProblems = () => API.get('/Problems');
export const addProblem = (problem) => API.post('/Problems', problem);

export const fetchContests = () => API.get('/contests');
export const addContest = (contest) => API.post('/contests', contest);
