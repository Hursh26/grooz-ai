
# GROOZ AI

Grooz AI is revolutionizing the way businesses interact with their customers online. Our state-of-the-art conversational AI solution seamlessly integrates with your website, empowering users to communicate naturally and get their tasks done efficiently.



## Deployment

To deploy this project, follow the steps below:

1. Clone the repository:

```bash
git clone (https://github.com/Hursh26/grooz-ai.git)
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Flask app:

```bash
python main.py
```

## API Reference
The API endpoints for the Grooz AI platform are as follows:

#### Get all items

```https://whisperapi.com/
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```https://developers.x.ai/python-sdk/grok/
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.


## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

- `API_KEY`: API key for the Whisper API
- `ANOTHER_API_KEY`: API key for the Grok API


## Features

- Voice Interaction
- Low Iteration
- Conversation History
- Seamless integration


## Installation

To install the necessary dependencies for this project, run the following command:

```bash
pip install -r requirements.txt
```
    
## Roadmap

- **Phase 1 (Done)**: A fully functional and efficient Voice bot, responds to the user as per query.
- **Phase 2**: Perform tasks on the website as per query. End to End interaction.
- **Phase 3**: Seamless Website integration with auto data indexing.

## Tech Stack

**Server**: Flask
