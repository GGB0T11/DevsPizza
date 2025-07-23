document.addEventListener("DOMContentLoaded", function () {
  const filterField = document.getElementById("filter-field");
  const valueTextInput = document.getElementById("value-text");
  const valueCategorySelect = document.getElementById("value-category");

  function toggleInputVisibility() {
    if (filterField.value === "category") {
      valueTextInput.style.display = "none";
      valueCategorySelect.style.display = "block";
      valueTextInput.name = "";
      valueCategorySelect.name = "value";
    } else {
      valueTextInput.style.display = "block";
      valueCategorySelect.style.display = "none";
      valueTextInput.name = "value";
      valueCategorySelect.name = "";
    }
  }

  toggleInputVisibility();

  filterField.addEventListener("change", toggleInputVisibility);
});
