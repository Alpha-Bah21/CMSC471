Feature: Shopping List Processing
  As a user
  I want to upload a handwritten shopping list photo
  So that it can be processed by AI and stored in the database

  Scenario: Upload a shopping list image
    Given I am on the Yellow Sign Diner dashboard
    When I click the UPLOAD button
    And I select a PNG image file
    Then the file should appear in the inbox list

  Scenario: Process a shopping list image
    Given I have a file selected in the inbox
    When I click the PROCESS button
    Then the activity log should show "Textract completed"
    And the records table should display the extracted items

  Scenario: Delete a file from inbox
    Given I have files in my inbox
    When I click the close button next to a file
    Then the file should be removed from the inbox list
    And the file should be deleted from S3

  Scenario: Delete a record from the records table
    Given I have records in the records table
    When I click the close button next to a record
    Then the record should be removed from the records table
    And the record should be deleted from DynamoDB

  Scenario: View health status
    Given the application is deployed
    When I navigate to /api/health
    Then I should see a JSON response with status ok
    And the response should include the current timestamp and region