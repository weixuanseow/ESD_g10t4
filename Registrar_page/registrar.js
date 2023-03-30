// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {
            patient_id: '',
            
        }
    },
    mounted() {

    },
    methods: {
        get_medicines(patient_id) {
            url = "http://127.0.0.1:5203/get_medicines/" + patient_id
            axios.get(url)
            .then(response => {
            this.message = response.data;
            console.log('done');
            })
            .catch(error => {
            console.log('error');
            console.log(error);
            })
    }}})
root.mount("#app")