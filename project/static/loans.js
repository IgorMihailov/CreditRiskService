url = "/add_loan"

let loans = [
  {
    amount: 10000,
    rate: 10,
    intent: 'EDUCATION',
    grade: 'B'
  },

  {
    amount: 20000,
    rate: 15,
    intent: 'PERSONAL',
    grade: 'B'
  },

  { 
    amount: 15000,
    rate: 8,
    intent: 'MEDICAL',
    grade: 'B'
  }
]

async function addLoan(id) {
    let loan;
    switch (id) {
      case 1:
        loan = loans[0];
        break;

      case 2:
        loan = loans[1];
        break;

      case 3:
        loan = loans[2];
        break;
      
      default:
        return "Error", 404
    }

    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(loan)
    })
    .then(response => { return response.text(); })
    .then(response => {
      console.log(response);
      alert(response);
    })
}