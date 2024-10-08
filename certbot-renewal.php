<?php
/*
Plugin Name: Certbot Renewal Handler
Description: Handles .well-known/acme-challenge file creation for Certbot renewals.
Version: 0.1
Author: Steve Hanlon
*/

if (!defined('ABSPATH')) {
    exit;
}

class Certbot_Renewal_Handler {

    private $challenge_dir;

    public function __construct() {
        // Set the challenge directory to the root of the web server
        $this->challenge_dir = $_SERVER['DOCUMENT_ROOT'] . '/.well-known/acme-challenge/';
        add_action('rest_api_init', [$this, 'register_rest_routes']);
    }

    // Register REST API route
    public function register_rest_routes() {
        register_rest_route('certbot/v1', '/challenge', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_challenge_file'],
            'permission_callback' => [$this, 'validate_request']
        ]);
    }

    // Permission callback (basic check, you can add authentication)
    public function validate_request() {
        return current_user_can('administrator'); // Adjust based on your needs
    }

    // Handle POST request to create/update challenge file
    public function handle_challenge_file(WP_REST_Request $request) {
        $filename = sanitize_file_name($request->get_param('filename'));
        $file_content = sanitize_textarea_field($request->get_param('content'));

        if (empty($filename) || empty($file_content)) {
            return new WP_Error('invalid_data', 'Filename or content is missing', ['status' => 400]);
        }

        // Ensure the directory exists
        if (!file_exists($this->challenge_dir)) {
            wp_mkdir_p($this->challenge_dir);
        }

        // Check if filename is restricted to .well-known/acme-challenge directory
        if (strpos($filename, '/') !== false) {
            return new WP_Error('invalid_filename', 'Invalid filename provided.', ['status' => 400]);
        }

        $file_path = $this->challenge_dir . $filename;
        if (file_put_contents($file_path, $file_content) === false) {
            return new WP_Error('file_error', 'Error writing file.', ['status' => 500]);
        }

        return new WP_REST_Response(['success' => true, 'file' => $file_path], 200);
    }
}

new Certbot_Renewal_Handler();

