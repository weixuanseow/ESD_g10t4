// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {

            something: '',

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
