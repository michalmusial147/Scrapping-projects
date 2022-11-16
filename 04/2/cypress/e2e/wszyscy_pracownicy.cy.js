Cypress.on('uncaught:exception', () => false)
describe('empty spec', () => {
  it('passes', () => {
    const fs = require('fs');

    cy.readFile('one_employee.json').then((text) => {
        console.log(text);
        text.forEach(element => {
          console.log(element);
          const imie = element.firstname;
          const nazwisko = element.lastname;
          cy.visit('https://adm.edu.p.lodz.pl/user/users.php')
          cy.get("#search").type(imie + " " + nazwisko)
          cy.get('.btn').contains('Wyszukaj w bazie wszystkich pracowników').click()
          cy.get(".btn").contains('Wyślij wiadomość').click()
          cy.get('#id_from').type("test")
          cy.get('#id_messageeditable').type("test")
          cy.get('#id_topic').type("test")
          cy.get('#id_submitbutton').click()
          cy.get('.alert').should("contain", 'Wiadomość wysłana')
          
        });

        

    })
  })
})