// send prescription details and patient allergies to the complex microservice
// function prescribeMedicine() {
//     var patientId = document.getElementById("patient-id").value;
//     var prescriptionDetails = [];
//     var medicineFields = document.getElementsByClassName("medicine-field");
//     for (var i = 0; i < medicineFields.length; i++) {
//         var medicine = {
//             med_name: medicineFields[i].querySelector('input[name="medicine[]"]').value,
//             frequency: medicineFields[i].querySelector('input[name="frequency[]"]').value,
//             amount: medicineFields[i].querySelector('input[name="amount[]"]').value
//         };
//         prescriptionDetails.push(medicine);
//     }
//     $.ajax({
//         url: "http://127.0.0.1:5101/prescribe_medicine",
//         type: "POST",
//         data: JSON.stringify({
//             patient_id: patientId,
//             prescription_details: prescriptionDetails,
//             // apptdate
//         }),
//         contentType: "application/json",
//         dataType: "json",
//         success: function(data) {
//             console.log("Flask responding", data);
//             if (data.code === 400 || data.code === 422) {
//                 // Display error message
//                 var errorMessage = data.message;
//                 $("#error-messages").html(errorMessage);
//             }
//             else if (data.code === 200){
//                 var showMessage = data.message;
//                 $("#error-messages").html(showMessage);
//             }
//         },
//         error: function(xhr, status, error) {
//             console.log("Error saving prescription:", xhr.responseText);
//         }
//     })
// }

var pid = sessionStorage.getItem('id')
var pdate = sessionStorage.getItem('date')
document.getElementById('patient-id').setAttribute('value',pid)
document.getElementById('patient-id').setAttribute('value',pid)

// var medicineCount = 1;

// function addMedicineFields() {
//     medicineCount++;

//     var medicineFields = document.getElementById("medicine-fields");

//     var medicineField = document.createElement("div");
//     medicineField.className = "medicine-field";

//     var medicineLabel = document.createElement("label");
//     medicineLabel.htmlFor = "medicine-" + medicineCount;
//     medicineLabel.innerHTML = "Medicine " + medicineCount + ":";

//     var medicineInput = document.createElement("input");
//     medicineInput.type = "text";
//     medicineInput.id = "medicine-" + medicineCount;
//     medicineInput.name = "medicine[]";

//     var frequencyLabel = document.createElement("label");
//     frequencyLabel.htmlFor = "frequency-" + medicineCount;
//     frequencyLabel.innerHTML = "Frequency " + medicineCount + ":";

//     var frequencyInput = document.createElement("input");
//     frequencyInput.type = "text";
//     frequencyInput.id = "frequency-" + medicineCount;
//     frequencyInput.name = "frequency[]";

//     var amountLabel = document.createElement("label");
//     amountLabel.htmlFor = "amount-" + medicineCount;
//     amountLabel.innerHTML = "Amount " + medicineCount + ":";

//     var amountInput = document.createElement("input");
//     amountInput.type = "text";
//     amountInput.id = "amount-" + medicineCount;
//     amountInput.name = "amount[]";

//     medicineField.appendChild(medicineLabel);
//     medicineField.appendChild(medicineInput);
//     medicineField.appendChild(document.createElement("br"));
//     medicineField.appendChild(frequencyLabel);
//     medicineField.appendChild(frequencyInput);
//     medicineField.appendChild(document.createElement("br"));
//     medicineField.appendChild(amountLabel);
//     medicineField.appendChild(amountInput);

//     medicineFields.appendChild(medicineField);
// }

// ---------------------------- VUE -----------------------------------------
// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {
            drugs: ["Acetaminophen",
            "aspirin",
            "Atorvastatin",
            "Ciprofloxacin",
            "Codeine",
            "Diazepam",
            "Doxycycline",
            "Fentanyl",
            "Fluoxetine",
            "Gabapentin",
            "Hydrochlorothiazide",
            "Ibuprofen",
            "Levothyroxine",
            "Lisinopril",
            "Lorazepam",
            "Losartan",
            "Metformin",
            "Metoprolol",
            "Naproxen",
            "Omeprazole",
            "Pantoprazole",
            "Paracetamol",
            "Prednisone",
            "Rosuvastatin",
            "Sertraline",
            "Simvastatin",
            "Tamsulosin",
            "Tramadol",
            "Venlafaxine",
            "Warfarin",
            "Zolpidem"],

            medicinecount: 0,
            medicines: [{ id: 1 }],

            selected_drug: [],

            message: '',
            // Suppose this is a very large array
            date_time: [],

            patients: [],

            rows: [],

            months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],

            datetosearch: '',

            medicine_fields: [],
        }
    },
    // mounted() {
    //     url = "http://127.0.0.1:5010/find_by_date/1"
    //     axios.get(url)
    //     .then(response =>(this.something = response.data.data.bookings))
    //     date = new Date()
    //     day = date.getDate()
    //     month = this.months[date.getMonth()]
    //     year = date.getFullYear()
    //     console.log(month)
    //     console.log(day)
    //     console.log(year)
    //     this.datetosearch += '11 Mar 2023' // put back to: day + ' ' + month + ' ' + year


    // },
    methods: {
        prescribe(date,id) {
            // alert(`it works! this is the id: ${date} this is the id: ${id}`)
            sessionStorage.setItem('date',date)
            sessionStorage.setItem('id',id)
            window.location.href = "../complex_prescribe_med/prescribe.html"
        },
        // create_patient_appoints_today() {
        //     console.log("=== [START] create_patient_appoints_today() ===")

        //     for(obj in this.something){
        //         // console.log(typeof(this.something[obj].appt_datetime))
        //         this.date_time.push(this.something[obj].appt_datetime)
        //         this.patients.push(this.something[obj].patient_id)
        //     }
            

        //     console.log(this.date_time[0])
            
        // },
        // addMedicineFields() {
        //     event.preventDefault()
        //     console.log("add fields called")
        //     // this.medicinecount += 1

        //     // var medicinefields = document.getElementById("medicine-fields")
        //     // medicinefields.innerHTML += `
        //     //     <label for="medicine-${this.medicinecount}">Medicine:</label>
        //     //     <select id="medicine-${this.medicinecount}" v-model="selected_drug">
        //     //         <option value="'" disabled selected>Choose Drug</option>
        //     //         <option v-for="drug in drugs" v-bind:value="drug" >{{ drug }}</option>
        //     //     </select><br>
        //     //     <label for="frequency-${this.medicinecount}">Frequency:</label>
        //     //     <input type="text" id="frequency-${this.medicinecount}" name="frequency[]"><br>
        //     //     <label for="amount-${this.medicinecount}">Amount:</label>
        //     //     <input type="text" id="amount-1" name="amount[]"><br>
        //     // `
        //     this.medicineCount++
        //     this.medicines.push({ id: this.medicineCount })
        //     console.log(this.medicine_fields)
        //   },
        addMedicineFields() {
            event.preventDefault();
            console.log("add fields called");
            // Get the parent container for the input fields
            var medicineFieldsContainer = document.querySelector("#medicine-fields");
            // Get the last input field set
            var lastMedicineFields = medicineFieldsContainer.childNodes[medicineFieldsContainer.childNodes.length - 2];
            // Clone the last input field set
            var newMedicineFields = lastMedicineFields.cloneNode(true);
            // Clear the ID attributes of the cloned input fields to avoid duplicates
            newMedicineFields.querySelectorAll("input, select").forEach((el) => {
                el.removeAttribute("id");
                el.value = ""; // reset the value to empty string
            });
            // Append the cloned input fields to the parent container
            medicineFieldsContainer.appendChild(newMedicineFields);
          },
        removeMedicineFields(index) {
            console.log("remove fields called")
            this.medicines.splice(index, 1)
        },
        prescribeMedicine() {
            let patientId = sessionStorage.getItem('id')
            var prescriptionDetails = [];
            var medicineFields = document.querySelectorAll('.medicine-field');
            console.log(medicineFields)
            for (var i = 0; i < medicineFields.length; i++) {
              var medicineNameInput = medicineFields[i].querySelector('select[id^="medicine-"]');
              var frequencyInput = medicineFields[i].querySelector('input[name="frequency[]"]');
              var amountInput = medicineFields[i].querySelector('input[name="amount[]"]');
              // Add error checking
              if (!medicineNameInput || !frequencyInput || !amountInput) {
                console.log('Error: missing input field');
              }
              console.log("Medicine name input:", medicineNameInput);
              console.log("Frequency input:", frequencyInput);
              console.log("Amount input:", amountInput);
          
              var medicine = {
                med_name: medicineNameInput.value,
                frequency: frequencyInput.value,
                amount: amountInput.value
              };
              console.log(medicine)
              prescriptionDetails.push(medicine);
            }
            console.log("this is the prescription details" + JSON.stringify(prescriptionDetails))
            $.ajax({
              url: "http://127.0.0.1:5101/prescribe_medicine/",
              type: "POST",
              data: JSON.stringify({
                patient_id: patientId,
                prescription_details: prescriptionDetails,
              }),
              contentType: "application/json",
              dataType: "json",
              success: function(data) {
                console.log("Flask responding", data);
                if (data.code === 400 || data.code === 422) {
                  var errorMessage = data.message;
                  $("#error-messages").html(errorMessage);
                } else if (data.code === 200) {
                  var showMessage = data.message;
                  $("#error-messages").html(showMessage);
                }
              },
              error: function(xhr, status, error) {
                console.log("Error saving prescription:", xhr.responseText);
              }
            })
          },
    },

})
root.component('medicine-field', {
    props: ['medicine', 'index', 'drugs'],
    template: `
    <div class="medicine-field">
    <label :for="'medicine-' + index">Medicine:</label>
    <select :id="'medicine-' + index" v-model="medicine.selected_drug">
      <option value="" disabled selected>Choose Drug</option>
      <option v-for="drug in drugs" :value="drug">{{ drug }}</option>
    </select>
    <button class="btn btn-warning" @click="$emit('remove-medicine')">Remove</button>
    <br>
    <label :for="'frequency-' + index">Frequency:</label>
    <input type="text" :id="'frequency-' + index" name="frequency[]"><br>
    <label :for="'amount-' + index">Amount:</label>
    <input type="text" :id="'amount-' + index" name="amount[]"><br>
  </div>
    `
  })
root.mount("#prescription")