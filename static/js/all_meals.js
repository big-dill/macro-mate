function setupSearch(userID, mealURL, apiURL) {
  const $select = $("#search").selectize({
    options: [],
    maxItems: 1,
    valueField: "id",
    labelField: "name",
    searchField: ["name"],
    persist: false,
    openOnFocus: false,
    closeAfterSelect: true,
    createOnBlur: true,
    create: false,
    onChange: function(value) {
      // Change window to the meal URL
      document.location.href = mealURL + value;
    },
    render: {
      option: function optionRenderer(item, escape) {
        return (
          '<div class="list-group">' +
          '<a class="text-body list-group-item" href="' +
          escape(mealURL) +
          escape(item.id) +
          '">' +
          escape(item.name) +
          "</a>" +
          "</div>"
        );
      },
    },
  });

  const $mealSearch = $select[0].selectize;
  // The following code is needed to prevent event propogation
  // so that the links will be registered on mouse up. Usually,
  // selectize will long close the list before this.

  // Ajax request to avoid getting tags from template
  // (Probably unsafe to mix python and js... also good demo of ajax call)

  $.get({
    url: apiURL,
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
