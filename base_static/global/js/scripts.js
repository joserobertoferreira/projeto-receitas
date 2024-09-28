function app_scope() {
  // esta função sai do escopo do navegador

  const forms = document.querySelectorAll(".form-delete");

  for (const form of forms) {
    form.addEventListener("submit", (event) => {
      event.preventDefault(); // prevenir a submissão do formulário

      const confirmed = confirm("Are you sure you want to delete this recipe?");

      if (confirmed) {
        // chamar a função que exclui o item com o id fornecido
        form.submit();
      }
    });
  }
}

app_scope();
