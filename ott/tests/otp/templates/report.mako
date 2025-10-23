<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP Test Report: ${now} - - ${num_passes} passes, ${num_errors} errors</title>
    <link href="https://cdn.datatables.net/2.0.3/css/dataTables.dataTables.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://cdn.datatables.net/2.0.3/js/dataTables.js"></script>
    <style>
        .FAIL {
            color: rgb(175, 0, 0);
        }
        .PASS {
            color: rgb(0, 175, 0);
        }
    </style>
    <!--
    TODO: have the request and response in a hidden / expandable row:
      https://datatables.net/examples/api/row_details.html
      https://live.datatables.net/bihawepu/1/edit
    -->
</head>
<body>
    <h1>OTP Test Report: ${now} - ${num_passes} passes, ${num_errors} errors</h1>
    <h2>Summary:</h2>
    <ul class="sweet_results">
    ${tsl.get_pass_fail_counts(True)}
    </ul>
    <br>
    <table id="tests" class="display" style="width:100%">
        <thead>
            <tr>
                <th>Test Suite</th>
                <th>#</th>
                <th>Result</th>
                <th>Description</th>
                <th>Diagnosis</th>
                <th>Request</th>
                <th>Response</th>
                <th>Expected</th>
            </tr>
        </thead>
        <tbody>
          %for ts in tsl.test_suites:
            %for t in ts.get_tests():
            <tr>
                <td><a target="_blank" href="${t.get_webapp_url()}">${ts.name}</a></td>
                <td><a target="_blank" href="${t.get_webapp_url()}">${t.csv_line_number}</a></td>
                <td>${t.get_result(True)}</td>
                <td>${t.description}</td>
                <td>${t.diagnosis}</td>
                <td>${t.get_payload(trim=300)}</td>
                <td>${t.get_itinerary(trim=300)}</td>
                <td>${t.expected}</td>
            </tr>
            %endfor
          %endfor
        </tbody>
    </table>
    <script>
        $(document).ready(function() {
            $('#tests').DataTable({
                scrollX: true,
                scrollY: 800
            });
        });
    </script>
</body>
</html>
