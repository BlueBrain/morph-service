
const { origin } = window.location;

export default {
  apiUrl: `${origin}${process.env.VUE_APP_BASE_URL}`,
  devUrl: 'http://localhost:8000',
};
