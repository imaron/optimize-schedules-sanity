#!/usr/bin/env python3
"""
Flask web service for schedule optimization.
Accepts Excel file upload, runs optimization, returns result.
"""

import os
import tempfile
from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename
import logging

# Import the optimization function
from optimize_schedules_with_sanity import (
    read_cost_pref_hours_caps, solve_cpsat, write_solution
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML template for the upload page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Schedule Optimizer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .upload-section {
            margin: 30px 0;
        }
        input[type="file"] {
            margin: 20px 0;
            padding: 10px;
            border: 2px dashed #4CAF50;
            border-radius: 5px;
            width: 100%;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #45a049;
        }
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .info {
            background-color: #e7f3fe;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
        }
        .requirements {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            display: none;
        }
        .status.processing {
            background-color: #fff3cd;
            display: block;
        }
        .status.success {
            background-color: #d4edda;
            display: block;
        }
        .status.error {
            background-color: #f8d7da;
            display: block;
        }
        ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        li {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📅 Schedule Optimizer</h1>

        <div class="info">
            <strong>ℹ️ How it works:</strong>
            <ul>
                <li>Upload your StaffScheduler.xlsx file</li>
                <li>The optimizer will assign employees to schedules based on costs and preferences</li>
                <li>Download the optimized file with assignments and a sanity check sheet</li>
            </ul>
        </div>

        <div class="requirements">
            <strong>📋 Excel File Requirements:</strong>
            <ul>
                <li>Day sheets (Mon-Sun) with COST, PREF, and HOURS data</li>
                <li>Weekly sheet with λ (preference weight), Max Shifts, and Max Hours</li>
                <li>See documentation for exact cell ranges</li>
            </ul>
        </div>

        <div class="upload-section">
            <form id="uploadForm" enctype="multipart/form-data">
                <label for="file"><strong>Select Excel File:</strong></label>
                <input type="file" id="file" name="file" accept=".xlsx" required>

                <button type="submit" id="submitBtn">Optimize Schedule</button>
            </form>
        </div>

        <div id="status" class="status"></div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const fileInput = document.getElementById('file');
            const submitBtn = document.getElementById('submitBtn');
            const statusDiv = document.getElementById('status');

            if (!fileInput.files.length) {
                statusDiv.className = 'status error';
                statusDiv.textContent = '❌ Please select a file';
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            submitBtn.disabled = true;
            statusDiv.className = 'status processing';
            statusDiv.textContent = '⏳ Processing... This may take up to 60 seconds.';

            try {
                const response = await fetch('/optimize', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'StaffScheduler_Optimized.xlsx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);

                    statusDiv.className = 'status success';
                    statusDiv.textContent = '✅ Success! Your optimized file has been downloaded.';
                } else {
                    const error = await response.text();
                    statusDiv.className = 'status error';
                    statusDiv.textContent = '❌ Error: ' + error;
                }
            } catch (error) {
                statusDiv.className = 'status error';
                statusDiv.textContent = '❌ Error: ' + error.message;
            } finally {
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page with upload form."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy'}, 200

@app.route('/optimize', methods=['POST'])
def optimize():
    """
    Accept Excel file upload, run optimization, return optimized file.
    """
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    if not file.filename.endswith('.xlsx'):
        return 'File must be an Excel file (.xlsx)', 400

    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # Save uploaded file
            input_path = os.path.join(tmpdir, secure_filename(file.filename))
            output_path = os.path.join(tmpdir, 'optimized_output.xlsx')

            logger.info(f"Saving uploaded file to {input_path}")
            file.save(input_path)

            # Read data
            logger.info("Reading Excel data...")
            costs, prefs, hours, lam, shift_caps, hour_caps = read_cost_pref_hours_caps(input_path)

            # Run optimization
            logger.info("Running optimization...")
            sol, obj = solve_cpsat(
                costs, prefs, hours, lam, shift_caps, hour_caps,
                max_time=60.0,
                workers=4
            )

            # Write solution
            logger.info("Writing solution...")
            write_solution(input_path, sol, obj, output_path, costs, hours, hour_caps)

            logger.info(f"Optimization complete. Objective: {obj:.2f}")

            # Send file back to user
            return send_file(
                output_path,
                as_attachment=True,
                download_name='StaffScheduler_Optimized.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        except Exception as e:
            logger.error(f"Error during optimization: {str(e)}", exc_info=True)
            return f'Optimization failed: {str(e)}', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
