/**
 * A function which sets up the search text box using the MealAPI view in the
 * API folder.
 *
 * @param {string} userID The user's ID so their meals can be fetched
 * @param {string} mealURL The URL which links to the meal's page
 * @param {string} apiURL The meal API URL which can fetch a user's / all meals
 */
function setupSearch(userID, mealURL, apiURL) {
  // Initialise selectize plugin
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
      // Change window to the meal URL on selection
      document.location.href = mealURL + value;
    },
    // A custom render html for each item in the dropdown list.
    render: {
      option: function optionRenderer(item, escape) {
        // escape is used for escaping dangerous html
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

  // AJAX call to the meal api
  $.get({
    url: apiURL,
    data: {
      user: userID ? userID : null,
    },
  }).done(function(response) {
    // Get the jquery plugin
    const $mealSearch = $select[0].selectize;
    $mealSearch.clearOptions();
    $mealSearch.load(function(callback) {
      callback(response);
    });
  });
}
