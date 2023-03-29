// send prescription details and patient allergies to the complex microservice
function prescribeMedicine() {
    var patientId = document.getElementById("patient-id").value;
    var prescriptionDetails = [];
    var medicineFields = document.getElementsByClassName("medicine-field");
    for (var i = 0; i < medicineFields.length; i++) {
        var medicine = {
            med_name: medicineFields[i].querySelector('input[name="medicine[]"]').value,
            frequency: medicineFields[i].querySelector('input[name="frequency[]"]').value,
            amount: medicineFields[i].querySelector('input[name="amount[]"]').value
        };
        prescriptionDetails.push(medicine);
    }
    $.ajax({
        url: "http://127.0.0.1:5101/prescribe_medicine",
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
                // Display error message
                var errorMessage = data.message;
                $("#error-messages").html(errorMessage);
            }
            else if (data.code === 200){
                var showMessage = data.message;
                $("#error-messages").html(showMessage);
            }
        },
        error: function(xhr, status, error) {
            console.log("Error saving prescription:", xhr.responseText);
        }
    })
}

var pid = sessionStorage.getItem('id')
var pdate = sessionStorage.getItem('date')
document.getElementById('patient-id').setAttribute('value',pid)
document.getElementById('patient-id').setAttribute('value',pid)
