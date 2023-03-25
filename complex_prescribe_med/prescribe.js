function submitPrescription() {
    var patientId = document.getElementById("patient-id").value;
    var medicines = [];
    var medicineFields = document.getElementsByClassName("medicine-field");
    for (var i = 0; i < medicineFields.length; i++) {
        var medicine = {
            med_name: medicineFields[i].querySelector('input[name="medicine[]"]').value,
            frequency: medicineFields[i].querySelector('input[name="frequency[]"]').value,
            amount: medicineFields[i].querySelector('input[name="amount[]"]').value
        };
        medicines.push(medicine);
    }
    $.ajax({
        url: "http://127.0.0.1:5050/patient/" + patientId + "/allergies",
        type: "GET",
        dataType: "json",
        success: function(response) {
            var allergies = response.join(',');
            prescribeMedicine(patientId, medicines, allergies);
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
}
    
// send prescription details and patient allergies to the complex microservice
function prescribeMedicine(patientId, prescriptionDetails, allergies) {
    $.post("http://127.0.0.1:5101/prescribe_medicine", {
      patient_id: patientId,
      prescription_details: prescriptionDetails,
      allergies: allergies
    }).done(function(data) {
      console.log("Prescription saved:", data);
    }).fail(function(xhr, status, error) {
      console.log("Error saving prescription:", xhr.responseText);
    });
  }
  