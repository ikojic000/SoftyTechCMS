var months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

$.ajax({
  url: "/api/users/count_by_months",
  type: "GET",
  success: function (data) {
    new Chart(document.getElementById("dashboard-users"), {
      type: "bar",
      data: {
        labels: months,
        datasets: [
          {
            label: "2023",
            backgroundColor: window.theme.primary,
            borderColor: window.theme.primary,
            hoverBackgroundColor: window.theme.primary,
            hoverBorderColor: window.theme.primary,
            data: data.usersCountList,
            barPercentage: 0.75,
            categoryPercentage: 0.5,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              gridLines: {
                display: false,
              },
              stacked: false,
            },
          ],
          xAxes: [
            {
              stacked: false,
              gridLines: {
                color: "transparent",
              },
            },
          ],
        },
      },
    });
  },
});

$.ajax({
  url: "/api/posts/count_by_months",
  type: "GET",
  success: function (data) {
    new Chart(document.getElementById("dashboard-articles"), {
      type: "bar",
      data: {
        labels: months,
        datasets: [
          {
            label: "2023",
            backgroundColor: window.theme.primary,
            borderColor: window.theme.primary,
            hoverBackgroundColor: window.theme.primary,
            hoverBorderColor: window.theme.primary,
            data: data.postsCountList,
            barPercentage: 0.75,
            categoryPercentage: 0.5,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              gridLines: {
                display: false,
              },
              stacked: false,
            },
          ],
          xAxes: [
            {
              stacked: false,
              gridLines: {
                color: "transparent",
              },
            },
          ],
        },
      },
    });
  },
});

$.ajax({
  url: "/api/comments/count_by_months",
  type: "GET",
  success: function (data) {
    new Chart(document.getElementById("dashboard-comments"), {
      type: "line",
      data: {
        labels: months,
        datasets: [
          {
            label: "2023",
            fill: true,
            backgroundColor: "transparent",
            borderColor: window.theme.primary,
            data: data.commentCountList,
          },
        ],
      },
      options: {
        scales: {
          xAxes: [
            {
              reverse: true,
              gridLines: {
                color: "rgba(0,0,0,0.05)",
              },
            },
          ],
          yAxes: [
            {
              borderDash: [5, 5],
              gridLines: {
                color: "rgba(0,0,0,0)",
                fontColor: "#fff",
              },
            },
          ],
        },
      },
    });
  },
});

// // Example starter JavaScript for disabling form submissions if there are invalid fields
// (function () {
//   "use strict";

//   // Fetch all the forms we want to apply custom Bootstrap validation styles to
//   var forms = document.querySelectorAll(".needs-validation");

//   // Loop over them and prevent submission
//   Array.prototype.slice.call(forms).forEach(function (form) {
//     form.addEventListener(
//       "submit",
//       function (event) {
//         if (!form.checkValidity()) {
//           event.preventDefault();
//           event.stopPropagation();
//         }

//         form.classList.add("was-validated");
//       },
//       false
//     );
//   });
// });
