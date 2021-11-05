// //дожидаемся полной загрузки страницы
//  window.onload = function () {
//
//     // получаем идентификатор элемента
//     var btn_submit = document.getElementById('submit');
//     var btn_check_phone = document.getElementById('check_phone');
//     alert("Здарова");
//
//     // вешаем на него событие
//     btn_submit.onclick = function() {
//
//       //const name = document.getElementById("name_").innerHTML
//
//         $.ajax({
//             url: '{{ url_for('view.path') }}',
//             type: 'POST',
//             data: {
//                 name: name
//             },
//             success: function (response) {
//             },
//             error: function (response) {
//             }
//         });
//
//     }
//
//     btn_check_phone.onclick = async function() {
//
//     }
//
//     const checkphone = async function() {
//
//     }
//
//     const start = async function() {
//         const result = await myfunction();
//         if (result == 0) {
//           alert ('Кредит одобрен!');
//         } else {
//           alert ('Кредит не одобрен!');
//         }
//     }
//
//     const myfunction = async function() {
//
//       let data = {
//         person_age: '66',
//         person_income: '42000',
//         person_emp_length: '2.0',
//         loan_amnt: '6475',
//         loan_int_rate: '9.99',
//         loan_percent_income: '0.15',
//         cb_person_cred_hist_length: '30',
//         person_home_ownership: 'RENT',
//         loan_intent: 'MEDICAL',
//         loan_grade: 'B',
//         cb_person_default_on_file: 'N',
//       };
//
//       let response = await fetch('http://localhost:5000/api/prediction', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json;charset=utf-8'
//       },
//       body: JSON.stringify(data)
//       });
//
//       let result = await response.json();
//       return result.prediction[0];
//     }
// }
