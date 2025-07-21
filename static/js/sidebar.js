document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.querySelector(".sidebar");
  const sidebarToggler = document.querySelector(".sidebar-toggler");

  if (sidebarToggler) {
    sidebarToggler.addEventListener("click", () => {
      sidebar.classList.toggle("collapsed");
      const icon = sidebarToggler.querySelector("span");
      icon.textContent = sidebar.classList.contains("collapsed")
        ? "chevron_right"
        : "chevron_left";
    });
  }
});

