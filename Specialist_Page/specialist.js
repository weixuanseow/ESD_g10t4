// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {

            something: {},

            // Suppose this is a very large array
            date_time: [],

            patients: [],

            rows: [],

            months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],

            datetosearch: '',
        }
    },
    mounted() {
        let appt = "2023-02-20 13:00:00"
        url = "http://127.0.0.1:5010/find_by_date/1"
        axios.get(url)
        .then(response =>(this.something = response.data.data.bookings))
        date = new Date()
        day = date.getDate()
        month = this.months[date.getMonth()]
        year = date.getFullYear()
        console.log(month)
        console.log(day)
        console.log(year)
        this.datetosearch += '11 Mar 2023' // put back to: day + ' ' + month + ' ' + year


    },
    methods: {
        prescribe(){
            alert("it works")
        },
        create_patient_appoints_today() {
            console.log("=== [START] create_patient_appoints_today() ===")

            for(obj in this.something){
                console.log(this.something[obj])
                this.date_time.push(this.something[obj].appt_datetime)
                this.patients.push(this.something[obj].patient_id)
            }



            console.log(this.date_time[0])

            let str =  `
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

            for(let i = 1; i <= this.something.length; i++) {
                todaysdate = this.datetosearch
                apptdate = this.date_time[i-1]
                if(apptdate.includes(todaysdate)){
                    temp = `<tr><td>`
                    temp += this.date_time[i-1]+ `</td><td>`+ this.patients[i-1]+ `</td><td><button class="btn btn-primary" v-on:click="prescribe">Prescribe Medicine</button> <button class="btn btn-warning">Book a Test</button></td></tr>`;
                    str += temp
                }
            }
            str += `</table>`
            console.log(document.getElementById('appointment'))
            console.log("=== [END] create_patient_appoints_today() ===")
            console.log(this.something)
            document.getElementById('appointment').innerHTML = str
        },


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






