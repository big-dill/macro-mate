function setupSearch(userID) {
  const $select = $("#search").selectize({
    options: [],
    valueField: "name",
    labelField: "name",
    searchField: ["name"],
    plugins: ["remove_button"],
    persist: false,
    openOnFocus: false,
    closeAfterSelect: true,
    createOnBlur: true,
    maxItems: 10,
    create: true,
  });

  const $mealSearch = $select[0].selectize;

  // Ajax request to avoid getting tags from template
  // (Probably unsafe to mix python and js... also good demo of ajax call)

  $.get({
    url: "/api/meals",
    data: {
      user: userID ? userID : null,
    },
  }).done(function(response) {
    $mealSearch.clearOptions();
    $mealSearch.load(function(callback) {
      callback(response);
    });
  });
}
