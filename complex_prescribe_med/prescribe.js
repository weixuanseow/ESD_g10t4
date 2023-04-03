var pid = sessionStorage.getItem('id')
var pdate = sessionStorage.getItem('date')
document.getElementById('patient-id').setAttribute('value',pid)
document.getElementById('patient-id').setAttribute('value',pid)


const root = Vue.createApp({
  data() {
      return {
          drugs: ["Acetaminophen",
          "Aspirin",
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

      patient_id: pid,
      appt_date: pdate,
      prescription_details: [
        {med_name:'', frequency:'', amount:''}
      ]
      }
    },
    methods: {
        prescribe(date,id) {
            sessionStorage.setItem('date',date)
            sessionStorage.setItem('id',id)
            window.location.href = "../complex_prescribe_med/prescribe.html"
        },
        addMedicine() {
          this.prescription_details.push({ med_name: '', frequency: '', amount: '' });
        },
        removeMedicine(index) {
            this.prescription_details.splice(index, 1)
        },
        prescribeMedicine() {
          const data = {
            patient_id: this.patient_id,
            prescription_details: this.prescription_details,
            appt_date: this.appt_date
          }
          console.log(data)
          $.ajax({
              url: "http://127.0.0.1:5101/prescribe_medicine",
              type: "POST",
              data: JSON.stringify(data),
              contentType: "application/json",
              dataType: "json",
              success: function(response) {
                  console.log("Flask responding", data);
                  if (response.code === 400 || response.code === 422) {
                      // Display error message
                      var errorMessage = response.message;
                      $("#error-messages").html(errorMessage);
                  }
                  else if (response.code === 200){
                      var showMessage = response.message;
                      $("#error-messages").html(showMessage);
                      window.location.href = "../Specialist_page/specialist_page.php"
                  }
              },
              error: function(error) {
                  console.log(error)
              }
          })
        }
    }

})
root.mount("#prescription")