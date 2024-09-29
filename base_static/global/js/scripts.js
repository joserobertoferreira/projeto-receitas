(() => {
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
})();

(() => {
  const buttonCloseMenu = document.querySelector(".button-close-menu");
  const buttonShowMenu = document.querySelector(".button-show-menu");
  const menuContainer = document.querySelector(".menu-container");

  const buttonShowMenuVisibleClass = "button-show-menu-visible";
  const menuHiddenClass = "menu-hidden";

  const closeMenu = () => {
    buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
    menuContainer.classList.add(menuHiddenClass);
  };

  const showMenu = () => {
    buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
    menuContainer.classList.remove(menuHiddenClass);
  };

  if (buttonCloseMenu) {
    buttonCloseMenu.removeEventListener("click", closeMenu);
    buttonCloseMenu.addEventListener("click", closeMenu);
  }

  if (buttonShowMenu) {
    buttonShowMenu.removeEventListener("click", showMenu);
    buttonShowMenu.addEventListener("click", showMenu);
  }
})();

(() => {
  const authorsLogoutLinks = document.querySelectorAll(".authors-logout-link");
  const formLogout = document.querySelector(".form-logout");

  for (const link of authorsLogoutLinks) {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      formLogout.submit();
    });
  }
})();
