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

            month_to_number: {'Jan': 1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
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
        booking(date,id){
            console.log(date)
            // console.log(this.something)
            // tempdate = date.slice(6, date.length - 4)
            // // console.log(tempdate)
            // tempstorage = tempdate.split(' ')
            // daynumber = tempstorage[0]
            // monthnumber = this.month_to_number[tempstorage[1]]
            // yearnumber = tempstorage[2]
            // const dateObj = new Date(date);
            // const newdate = `${yearnumber}-${monthnumber}-${daynumber} ${dateObj.toLocaleTimeString()}`;
            //newdate =  yearnumber + '-' + monthnumber + '-' + daynumber + ' ' + tempstorage[3]
            const newdate = this.formatDate(date);
            console.log(newdate)
            sessionStorage.setItem('appt',newdate)
            sessionStorage.setItem('pid',id)
            window.location.href = "../booking/booking.html"
        },
        prescribe(date,id) {
            alert(`it works! this is the id: ${date} this is the id: ${id}`)
                        console.log(date)
            console.log(date)
            console.log(this.something)
            tempdate = date.slice(6, date.length - 4)
            console.log(tempdate)
            tempstorage = tempdate.split(' ')
            daynumber = tempstorage[0]
            monthnumber = this.month_to_number[tempstorage[1]]
            yearnumber = tempstorage[2]
            const newdate = `${yearnumber}-${monthnumber}-${daynumber} ${dateObj.toLocaleTimeString()}`;
            console.log(newdate)

            sessionStorage.setItem('appt',newdate)
            sessionStorage.setItem('id',id)
            window.location.href = "../complex_prescribe_med/prescribe.html"
        },
        create_patient_appoints_today() {
            console.log("=== [START] create_patient_appoints_today() ===")

            for(obj in this.something){
                // console.log(typeof(this.something[obj].appt_datetime))
                this.date_time.push(this.something[obj].appt_datetime)
                this.patients.push(this.something[obj].patient_id)
            }
            

            console.log(this.date_time[0])

            // let str =  `
            // <table id="appointment_table" border="2px">
            // <tr>
            //     <th>
            //         <h2>Date&Time</h2>
            //     </th>

            //     <th>
            //         <h2>Patient</h2>
            //     </th>

            //     <th>
            //         <h2>Select</h2>
            //     </th>

            // </tr>
            // `

            // for(let i = 1; i <= this.something.length; i++) {
            //     todaysdate = this.datetosearch
            //     apptdate = this.date_time[i-1]  
            //     if(apptdate.includes(todaysdate)){
            //         temp = `<tr><td>`
            //         button = document.createElement('button')
            //         button.setAttribute('class','btn btn-primary')
            //         button.setAttribute('v-on:click','prescribe')
            //         button.innerText = 'Prescribe Medicine'
            //         temp += this.date_time[i-1]+ `</td><td>`+ this.patients[i-1]+ `</td><td><button class="btn btn-primary" @click="prescribe">Prescribe Medicine</button> <button class="btn btn-warning">Book a Test</button></td></tr>`;
            //         str += temp
            //     }
            // }
            // str += `</table>`
            // console.log(document.getElementById('appointment'))
            // console.log("=== [END] create_patient_appoints_today() ===")
            // console.log(this.something)
            // document.getElementById('appointment').innerHTML = str

            
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            const year = date.getUTCFullYear();
            const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
            const day = date.getUTCDate().toString().padStart(2, '0');
            const hours = date.getUTCHours().toString().padStart(2, '0');
            const minutes = date.getUTCMinutes().toString().padStart(2, '0');
            const seconds = date.getUTCSeconds().toString().padStart(2, '0');
          
            const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
            return formattedDate;
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

