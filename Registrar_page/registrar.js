// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {
            patient_id: '',
            appt_date: '',
            top_up_message: ''
        }
    },
    created() {
        // SocketIO server, listen for top_up_message event
        const socket = io.connect('http://localhost:5204/');
        socket.on('top_up_message', (message) => {
            console.log(message)
            alert(message)
            this.top_up_message = message;
            document.getElementById('topup').innerHTML='<h2>' + message+'</h2>'
        });
    },
    mounted() {
        date = new Date();
        date = date.toISOString().substring(0,10);
        console.log(date, 'mounted')
        patient_id=document.getElementById("patient_id").value
        console.log(patient_id, 'mounted')

    },
    methods: {
        // Method to get medicines for the patient
        get_medicines() {
            patient_id=document.getElementById("patient_id").value
            console.log(typeof(patient_id))
            console.log(typeof(date))
            const url = "http://127.0.0.1:5204/get_medicines/" + patient_id + "/" + date;

            axios.get(url)
            .then(response => {
                const prescriptions = response.data.data;
                let FISH = '<table><tr><th>Medicine</th><th>Amount</th></tr>';
                for (let prescription in prescriptions) {
                    console.log(prescription);
                    console.log(prescriptions[prescription]);
                    FISH += '<tr><td>' + prescription + '</td><td>' + prescriptions[prescription] + '</td></tr>';
                }
                FISH += '</table>';
                document.getElementById("medicines").innerHTML = FISH;
            })
            .catch(error => {
                console.log('error');
                console.log(error);
            });
       
          }
    }
})
root.mount("#dispense")