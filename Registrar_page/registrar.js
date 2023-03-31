// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {
            patient_id: '',
            appt_date: ''
        }
    },
    mounted() {
        date = new Date();
        date = date.toISOString().substring(0,10);
        date = "2023-02-20" //comment this out later!
        console.log(date, 'mounted')
        patient_id=document.getElementById("patient_id").value
        console.log(patient_id, 'mounted')
    },
    methods: {
        get_medicines() {
            patient_id=document.getElementById("patient_id").value
            console.log(patient_id, 'method')
            console.log(date, 'method')
            url = "http://127.0.0.1:5203/get_medicines/" + patient_id + "/" + date
            axios.get(url)
            .then(response => {
            this.message = response.data;
            console.log(response) // comment out ltr
            console.log(this.message) // comment out ltr
            console.log('done');
            })
            .catch(error => {
            console.log('error');
            console.log(error);
            })
    }}})
root.mount("#dispense")