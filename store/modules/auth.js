import axios from 'axios'
import router from '@/router'

const state = {
    email: null,
	token: null,
};

const mutations = {
	authUser(state, userData) {
		state.email = userData.email;
		state.token = userData.token;
	},
	clearAuthData(state) {
		state.email = null;
		state.token = null;
	},
};

const getters = {
	isAuthenticated(state) {
		return state.token !== null;
	},
};

const actions = {
	login: ({commit}, authData) => {
		axios.post('/api/v1/login', {
            email: authData.email,
			password: authData.password,
		}).then(response => {
			let success = response.data.success;
			if (success === true) {
				commit('authUser', { email: authData.email, token: response.data.token });
				localStorage.setItem('token', response.data.token);
				localStorage.setItem('email', authData.email);
				router.replace('newTask')
			}
			else {
				console.log('Login error');
			}
		}).catch(error => {
			console.log(error);
		})
	},
	autoLogin({commit}) {
		let token = localStorage.getItem('token');
		let email = localStorage.getItem('email');

		if (!token || !email) {
			return;
		}

		commit('authUser', { email: email, token: token });
	},
	logout: ({commit}) => {
		commit('clearAuthData');
		localStorage.removeItem('email');
		localStorage.removeItem('token');
		router.replace('login');
	},
};

export default {
	namespaced: true,
	state,
	mutations,
	getters,
	actions,
}
