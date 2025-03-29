# Silicon Valley Visit Planner

A Streamlit-based web application for planning and sharing experiences about visiting Silicon Valley. The app includes features for user authentication, interactive chat with Langflow, and a community platform for sharing experiences.

## Features

- User authentication (login/register)
- Interactive chat interface connected to Langflow
- Example visit planning guide
- Community platform for sharing experiences
- Three-stage visit planning structure:
  1. Pre-Visit Planning
  2. During Visit
  3. Post-Visit Impact

## Setup

### Setup the virtual environment

```bash
mkdir .venv
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install uv
uv venv
source .venv/bin/activate

uv pip install -r requirements.txt

```

-- to disable use
deactivate

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create an `assets` directory and add the following images:

   - `sv_header.jpg` (main header image)
   - `google_campus.jpg` (Google campus image)
   - `apple_park.jpg` (Apple Park image)

4. Start the Langflow server (required for the chat feature):

   ```bash
   langflow run
   ```

5. Run the Streamlit app:
   ```bash
   streamlit run Home.py
   ```

## Project Structure

- `app.py`: Main application file with authentication and home page
- `pages/1_Example_Visit.py`: Example visit planning guide
- `pages/2_Interactive_Chat.py`: Chat interface connected to Langflow
- `pages/3_Community.py`: Community platform for sharing experiences
- `requirements.txt`: Project dependencies
- `assets/`: Directory for storing images
- `users.json`: User authentication data
- `community_posts.json`: Community posts data

## Usage

1. Register a new account or login with existing credentials
2. Navigate through different pages using the sidebar
3. Use the interactive chat to get personalized recommendations
4. Share your experiences in the community section
5. Filter and read posts from other community members

## Requirements

- Python 3.8+
- Streamlit
- Langflow
- Python-dotenv
- Pillow

## Contributing

Feel free to submit issues and enhancement requests!
