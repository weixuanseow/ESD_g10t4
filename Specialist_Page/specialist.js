// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {

            something: [],

            // Suppose this is a very large array
            date_time: [
                '23/03/23 0900HRS',
                '23/03/23 1000HRS',
                '23/03/23 1100HRS',
                '23/03/23 1200HRS',
                '23/03/23 1300HRS'
            ],
            patients: [
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            rows: [
                '1',
                '2',
                '3',
                '4',
                '5',
            ],


        }
    },
    mounted() {
        let appt = "2023-02-20 13:00:00"
        url = "http://127.0.0.1:5100/patient/000000001"
        axios.get(url)
        .then(response =>(this.something = response.data.phone))
    },

    methods: {

        // say_hello() {
        //     console.log("=== [START] say_hello() ===")
        //     console.log("=== [END] say_hello() ===")
        //     return Date.now()
        // },

        create_patient_appoints_today() {
            console.log("=== [START] create_patient_appoints_today() ===")
            let str = `
            <table id="appointment_table" border="2px">
            <tr>
                <th>
                    <h2>Date&Time</h2>
                </th>

                <th>
                    <h2>Patient</h2>
                </th>

                <th>
                    <h2>Select</h2>
                </th>

            </tr>
            `

            for(let i = 1; i <= this.rows.length; i++) {
                temp = `<tr><td>`
                temp += this.date_time[i-1]+ `</td><td>`+ this.patients[i-1]+ `</td><td><button class="btn btn-primary">Prescribe Medicine</button> <button class="btn btn-warning">Book a Test</button></td></tr>`;
                str += temp
            }
            str += `</table>`
            console.log(document.getElementById('appointment'))
            console.log("=== [END] create_patient_appoints_today() ===")
            console.log(this.something)
            document.getElementById('appointment').innerHTML = str
        }

    },
        // computed: {

    //     say_bye() {
    //         console.log("=== [START] say_bye() ===")
    //         console.log("=== [END] say_bye() ===")
    //         return Date.now()
    //     },

    //     make_fruit_string_again() {
    //         console.log("=== [START] make_fruit_string_again() ===")
    //         let str = ""

    //         for(let i = 1; i <= this.fruits.length; i++) {
    //             if( (i % 2) === 0 ) {
    //                 // even number
    //                 str += this.fruits[i-1].toUpperCase() + ", "
    //             }
    //             else {
    //                 str += this.fruits[i-1].toLowerCase() + ", "
    //             }
    //         }
    //         console.log("=== [END] make_fruit_string_again() ===")

    //         return str.slice(0, -2)
    //     }
    // }

})
root.mount("#appointment")

// function getPatient(){
//     // Get patient phone number here and store in session
//     // These info should be taken from periovus page
//     // let pid = 000000001 // maybe pid now need get from session
//     let appt = "2023-02-20 13:00:00"
//     // sessionStorage.getItem("pid",pid)
//     // sessionStorage.getItem('appt',appt)
//     // 
//     // test_type = document.getElementById('test_type').value
//     url = "http://127.0.0.1:5100/appointment_history/" + appt
//     axios.get(url)
//     .then(response =>{
//         data = response.data
//         console.log(data)
//         //storing pid, phone and visit_type in session

//         // let phone = data.data.phone

//         // these data needs to be used in next page , assume first page send to this page through session storage

//         // sessionStorage.setItem('phone',phone)
//         // sessionStorage.setItem("test_type",test_type)
//         // console.log(test_type + "Test Type retrieved and "+ "patient details:" + pid + " and " + phone)
//         // window.location.href="getslots.html"

//     })
//     .catch((error) => {
//             const errorCode = error.code;
//             const errorMessage = error.message;
//             console.log(errorMessage)
//         });


// }






