import second from 'axios'

export const getLoginToken = () => {
	axios.get('http://localhost:8000/auth/login/')
}
