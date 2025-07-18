document.addEventListener("DOMContentLoaded", function () {
  const filterField = document.getElementById("filter-field");
  const valueTextInput = document.getElementById("value-text");
  const valueRoleSelect = document.getElementById("value-role");

  function toggleInputVisibility() {
    if (filterField.value === "role") {
      valueTextInput.style.display = "none";
      valueRoleSelect.style.display = "block";
      valueTextInput.name = "";
      valueRoleSelect.name = "value";
    } else {
      valueTextInput.style.display = "block";
      valueRoleSelect.style.display = "none";
      valueTextInput.name = "value";
      valueRoleSelect.name = "";
    }
  }

  toggleInputVisibility();

  filterField.addEventListener("change", toggleInputVisibility);
});
