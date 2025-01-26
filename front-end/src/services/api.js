import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Flask backend URL
});

// User-related API calls
export const fetchUsers = () => API.get('/users');
export const addUser = (user) => API.post('/users', user);

// Problem-related API calls
export const fetchProblems = () => API.get('/Problems');
export const addProblem = (problem) => API.post('/Problems', problem);

// Contest-related API calls
export const fetchContests = () => API.get('/contests');
export const addContest = (contest) => API.post('/contests', contest);

// // Fetch problems for a specific contest
export const getContestProblems = (contestId) => API.get(`/contest_problems/${contestId}`);

export const getContestByID = (contestId) => API.get(`/contests/${contestId}`)
