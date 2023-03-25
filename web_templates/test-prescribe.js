// import React, { useState } from 'react';

// function DoctorPrescription() {
//   const [patientId, setPatientId] = useState('');
//   const [medicine, setMedicine] = useState('');
//   const [dosage, setDosage] = useState('');
//   const [notes, setNotes] = useState('');
//   const [interaction, setInteraction] = useState(null);
//   const [allergy, setAllergy] = useState(null);
//   const [prescriptionStatus, setPrescriptionStatus] = useState('pending');
//   const [prescriptionHistory, setPrescriptionHistory] = useState([]);

//   const handlePatientIdChange = (event) => {
//     setPatientId(event.target.value);
//   }

//   const handleMedicineChange = (event) => {
//     setMedicine(event.target.value);
//   }

//   const handleDosageChange = (event) => {
//     setDosage(event.target.value);
//   }

//   const handleNotesChange = (event) => {
//     setNotes(event.target.value);
//   }

//   const handlePrescriptionSubmit = (event) => {
//     event.preventDefault();
//     // Check for drug interactions and allergies using OpenFDA API
//     const openFdaUrl = `https://api.fda.gov/drug/label.json?search=active_ingredient:${prescription.drugName}`;
//     fetch(openFdaUrl)
//         .then((response) => response.json())
//         .then((data) => {
//         const drugInteractions = data.results[0].drug_interactions;
//         const contraindications = data.results[0].contraindications;

//       // Check for drug interactions
//       if (drugInteractions.length > 0) {
//         alert(`Warning: Drug interactions detected!\n${drugInteractions.join("\n")}`);
//       }

//       // Check for allergies
//       const allergies = prescription.patient.allergies;
//       if (allergies && allergies.length > 0) {
//         const allergens = data.results[0].allergens;
//         const allergyMatch = allergens.find((allergen) => allergies.includes(allergen));
//         if (allergyMatch) {
//           alert(`Warning: Patient is allergic to ${allergyMatch}!`);
//         }
//       }
//     // If there are no issues, submit the prescription to the server and update prescription status
//     setPrescriptionStatus('submitted');
//   }

//   const handlePrescriptionPickup = () => {
//     // Add logic here to notify the doctor when the prescription is ready for pickup
//     setPrescriptionStatus('ready');
//   }

//   return (
//     <div>
//       <h2>Doctor Prescription</h2>
//       <form onSubmit={handlePrescriptionSubmit}>
//         <div>
//           <label htmlFor="patientId">Patient ID:</label>
//           <input type="text" id="patientId" name="patientId" value={patientId} onChange={handlePatientIdChange} />
//         </div>
//         <div>
//           <label htmlFor="medicine">Medicine:</label>
//           <input type="text" id="medicine" name="medicine" value={medicine} onChange={handleMedicineChange} />
//         </div>
//         <div>
//           <label htmlFor="dosage">Dosage:</label>
//           <input type="text" id="dosage" name="dosage" value={dosage} onChange={handleDosageChange} />
//         </div>
//         <div>
//           <label htmlFor="notes">Notes:</label>
//           <textarea id="notes" name="notes" value={notes} onChange={handleNotesChange} />
//         </div>
//         {interaction && <p className="error">{interaction}</p>}
//         {allergy && <p className="error">{allergy}</p>}
//         {prescriptionStatus === 'ready' && <p>Your prescription is ready for pickup!</p>}
//         {prescriptionStatus === 'pending' && <button type="submit">Submit Prescription</button>}
//         {prescriptionStatus === 'submitted' && <button disabled>Pending Pickup</button>}
//       </form>
//     </div>
//   );
// }

// export default DoctorPrescription;
