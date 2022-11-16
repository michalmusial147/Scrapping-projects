Cypress.on('uncaught:exception', () => false)
describe('Test message.', () => {
  it('passes', () => {
    cy.visit('https://adm.edu.p.lodz.pl/user/users.php')
    cy.get("#search").type('Rafał')
    cy.get('.btn').contains('Wyszukaj w bazie wszystkich pracowników').click()
    cy.get(".btn").contains('Wyślij wiadomość').click()
    cy.get('#id_from').type("test")
    cy.get('#id_messageeditable').type("test")
    cy.get('#id_topic').type("test")
    cy.get('#id_submitbutton').click()
    cy.get('.alert').should("contain", 'Wiadomość wysłana')
  })
})