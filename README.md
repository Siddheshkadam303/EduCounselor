 🎓 EduCounselor - AI-Powered Educational Guidance Assistant

A sophisticated Flask-based web application that provides intelligent educational counseling and guidance using Google's Gemini AI. EduCounselor helps parents and students navigate educational programs, course offerings, pricing information, and school partnerships through an interactive chat interface.

 🌟 Features

 🤖 AI-Powered Conversations
- Advanced Language Model: Powered by Google's Gemini 2.0 Flash model
- Context-Aware Responses: Maintains conversation history for coherent interactions
- Document-Based Knowledge: Extracts and processes information from PDF documents
- Persistent Chat History: Saves conversations across sessions

 📚 Educational Expertise
- Course and program information
- Pricing and scheduling details
- School partnership opportunities
- Career counseling methodologies
- Age-appropriate guidance approaches
- Parent engagement strategies

 💬 Modern Chat Interface
- Responsive Design: Works seamlessly on desktop and mobile devices
- Real-time Messaging: Instant responses with typing indicators
- Quick Questions: Pre-defined buttons for common inquiries
- Feedback System: Users can rate responses to improve service quality
- Auto-resizing Input: Dynamic textarea that expands with content

 🔧 Technical Features
- Vector Search: Uses ChromaDB for efficient document retrieval
- PDF Processing: Automatic text extraction from educational documents
- Persistent Storage: Maintains vector embeddings and chat history
- Error Handling: Robust error management and user feedback
- RESTful API: Clean endpoints for chat and feedback functionality

 🚀 Live Demo

🌐 [Access EduCounselor Live](https://educounselor.onrender.com/)
Hosted on Render - Professional cloud hosting platform

 🛠️ Installation & Setup

 Prerequisites
- Python 3.8 or higher
- pip package manager
- Google AI API key (Gemini)

 1. Clone the Repository
```bash
git clone https://github.com/Siddheshkadam303/EduCounselor.git
cd EduCounselor
```

 2. Install Dependencies
```bash
pip install -r requirements.txt
```

 3. Environment Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

 4. Document Setup
1. Create a `docs` folder in the project root
2. Place your educational PDF documents in the `docs` folder
3. The application will automatically extract text from PDFs on first run

 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

 📦 Dependencies

 Core Framework
- Flask: Web application framework
- Python-dotenv: Environment variable management

 AI & Machine Learning
- LangChain: LLM application framework
- Google Generative AI: Gemini model integration
- ChromaDB: Vector database for embeddings
- PyMuPDF (fitz): PDF text extraction

 Additional Libraries
- Requests: HTTP library for API calls
- Logging: Application monitoring and debugging

 🏗️ Project Structure

```
EduCounselor/
├── app.py                       Main Flask application
├── requirements.txt             Python dependencies
├── .env                         Environment variables (create this)
├── docs/                        PDF documents folder
├── static/
│   ├── style.css               Modern CSS styling
│   └── script.js               Frontend JavaScript
├── templates/
│   └── index.html              Main chat interface
├── chat_history_parent.json    Persistent chat history
├── parent_faq.txt              Extracted PDF text
└── retriever_store_parent/     Vector embeddings storage
```

 🔧 Configuration

 Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key for AI functionality

 Customization Options
- Document Source: Change PDF folder path in `app.py`
- Chat History: Modify history file name and location
- Vector Store: Customize embedding storage directory
- Model Parameters: Adjust chunk size, overlap, and retrieval count

 🌐 Deployment

 Render Deployment (Recommended)
1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy with automatic builds on git push

 Alternative Deployment Options
- Heroku: Cloud platform with git-based deployment
- Vercel: Serverless deployment platform
- Railway: Modern cloud deployment
- Docker: Containerized deployment

 🎯 Usage Examples

 Quick Start Questions
- "What counseling courses do you offer?"
- "What are your pricing plans?"
- "Do you partner with schools?"
- "How do I get started?"

 Advanced Queries
- "What's the best program for a 15-year-old interested in STEM?"
- "How do your school partnership programs work?"
- "What career counseling methodologies do you use?"
- "Can you explain your pricing structure for group sessions?"

 🤝 Contributing

We welcome contributions to improve EduCounselor! Here's how you can help:

1. Fork the Repository
2. Create a Feature Branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit Your Changes
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. Push to Branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

 Areas for Contribution
- 🎨 UI/UX improvements
- 🔧 Performance optimizations
- 📱 Mobile responsiveness enhancements
- 🌍 Internationalization support
- 📊 Analytics and reporting features
- 🔒 Security enhancements

 🐛 Troubleshooting

 Common Issues

PDF Processing Errors
- Ensure PDFs are readable and not password-protected
- Check that the `docs` folder exists and contains PDF files

API Key Issues
- Verify your Gemini API key is valid and has sufficient quota
- Ensure the `.env` file is properly configured

Vector Store Problems
- Delete the `retriever_store_parent` folder to rebuild embeddings
- Check disk space for vector storage

Chat History Issues
- Delete `chat_history_parent.json` to reset conversation history
- Verify file permissions for read/write access

🙏 Acknowledgments

- Google AI: For providing the powerful Gemini language model
- LangChain: For the excellent LLM application framework
- ChromaDB: For efficient vector storage and retrieval
- Flask Community: For the robust web framework
- Render: For reliable cloud hosting services

 📞 Support & Contact

- Issues: [GitHub Issues](https://github.com/Siddheshkadam303/EduCounselor/issues)
- Discussions: [GitHub Discussions](https://github.com/Siddheshkadam303/EduCounselor/discussions)
- Email: [kadamsiddhesh1104@gmail.com]
- LinkedIn: [ https://www.linkedin.com/in/siddhesh-kadam-84292a256/ ]

 🔮 Future Enhancements

- 📊 Analytics dashboard for usage insights
- 🎯 Multi-language support
- 📱 Mobile app development
- 🔗 Integration with popular educational platforms
- 🤖 Advanced AI features and personalization
- 📈 Performance monitoring and optimization
- 🔐 User authentication and profiles

---

⭐ If you found this project helpful, please consider giving it a star on GitHub!

Built with ❤️ by [Siddhesh Kadam](https://github.com/Siddheshkadam303)
