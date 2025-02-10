function toggleSidebar() {
  let sidebar = document.getElementById("sidebar");

  if (sidebar.classList.contains("hidden")) {
    sidebar.classList.remove("hidden");
  } else {
    sidebar.classList.add("hidden");
  }
}

function toggleListMenu() {
  let listMenu = document.getElementById("list-menu")

  if (listMenu.classList.contains("hidden")) {
    listMenu.classList.remove("hidden");
  } else {
    listMenu.classList.add("hidden");
  }
}