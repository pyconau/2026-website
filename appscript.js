// Replace 'DISCORD_WEBHOOK_URL' with your actual Discord webhook URL
const DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1447148269443743827/2S3J7fhnJReu33OzYaTOGLVpvqPE66nPkot8Ek3objmIkmC4X5ZQRh_gL8HRWDy90f_W';


function onSubmitDoSendToDiscord(e) {
  try {
    // Log the event object for debugging
    Logger.log('Event object: ' + JSON.stringify(e));

    // Check if response exists and has the expected methods
    if (!e || !e.response || typeof e.response.getItemResponses !== 'function') {
      let eventStr;
      try {
        eventStr = JSON.stringify(e);
      } catch (stringifyError) {
        eventStr = 'Unable to stringify event object';
      }
      const errorMsg = 'Invalid event object. This trigger must be set to "On form submit" (not time-based or manual). Event: ' + eventStr;
      Logger.log(errorMsg);
      sendToDiscord(errorMsg);
      return; // Exit without throwing to avoid double error messages
    }

    const response = e.response;

    const itemResponses = response.getItemResponses();

    let message = "New Google Form Submission:\n";

    for (const itemResponse of itemResponses) {
      const question = itemResponse.getItem().getTitle();
      const answer = itemResponse.getResponse();
      message += `${question}: ${answer}\n`;
    }

    // Get the submitter's email address (only works if form requires sign-in)
    try {
      const respondentEmail = response.getRespondentEmail();
      if (respondentEmail) {
        message += `Submitter's Email: ${respondentEmail}\n`;
      }
    } catch (emailError) {
      Logger.log('Could not get respondent email: ' + emailError);
      // Continue without email if it's not available
    }

    sendToDiscord(message);

  } catch (error) {
    Logger.log('Error in onSubmit: ' + error);
    // Send error notification to Discord
    sendToDiscord('Error processing form submission: ' + error.message);
    throw error; // Re-throw to see in execution log
  }
}

function sendToDiscord(message) {
  try {
    // Ensure message is a string
    let messageStr;
    if (typeof message === 'string') {
      messageStr = message;
    } else {
      try {
        messageStr = JSON.stringify(message);
      } catch (e) {
        messageStr = String(message);
      }
    }

    // Log what we're about to send
    Logger.log('Sending to Discord: ' + messageStr.substring(0, 200));

    // Discord has a 2000 character limit for message content
    const truncatedMessage = messageStr.length > 2000 ? messageStr.substring(0, 1997) + '...' : messageStr;

    const payload = {
      content: truncatedMessage,
    };

    const payloadJson = JSON.stringify(payload);
    Logger.log('Payload JSON: ' + payloadJson.substring(0, 200));

    const options = {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      payload: payloadJson,
    };

    const response = UrlFetchApp.fetch(DISCORD_WEBHOOK_URL, options);
    Logger.log('Discord response: ' + response.getResponseCode());
  } catch (error) {
    Logger.log('Error in sendToDiscord: ' + error);
    throw error;
  }
}

// Example: Test the webhook with curl
// curl -X POST "https://discord.com/api/webhooks/1447148269443743827/2S3J7fhnJReu33OzYaTOGLVpvqPE66nPkot8Ek3objmIkmC4X5ZQRh_gL8HRWDy90f_W" \
//   -H "Content-Type: application/json" \
//   -d '{"content": "Test message from curl - webhook is working!"}'