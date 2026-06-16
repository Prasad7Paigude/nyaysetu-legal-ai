// Platform Documentation Content

export interface DocPage {
  id: string;
  title: string;
  content: string;
}

export interface DocSection {
  id: string;
  title: string;
  pages: DocPage[];
}

export const platformDocs: DocSection[] = [
  // 1. INTRODUCTION
  {
    id: "introduction",
    title: "Introduction",
    pages: [
      {
        id: "what-is-nyaysetuai",
        title: "What is NyaySetuAI?",
        content: `
          <h2>What is NyaySetuAI?</h2>
          <p>NyaySetuAI is an <strong>AI-powered legal assistance platform</strong> designed to make legal information and services accessible to every citizen in India. The platform bridges the gap between complex legal systems and ordinary people who need legal help but may not have access to expensive lawyers or legal consultants.</p>
          
          <h3>The Problem We Solve</h3>
          <p>Many citizens face challenges when dealing with legal matters:</p>
          <ul>
            <li><strong>Language Barrier:</strong> Legal documents use complex terminology that's hard to understand</li>
            <li><strong>Cost:</strong> Hiring lawyers is expensive, even for simple legal queries</li>
            <li><strong>Access:</strong> Not everyone has easy access to legal professionals</li>
            <li><strong>Awareness:</strong> Most people don't know their legal rights or which laws apply to their situation</li>
            <li><strong>Time:</strong> Getting legal help often takes days or weeks</li>
          </ul>

          <h3>Our Solution</h3>
          <p>NyaySetuAI provides <strong>instant, free, and easy-to-understand legal assistance</strong> using artificial intelligence. Whether you need to:</p>
          <ul>
            <li>Understand which IPC (Indian Penal Code) sections apply to your case</li>
            <li>Draft legal documents like FIRs, RTI applications, or legal notices</li>
            <li>Get simple explanations of complex legal concepts</li>
            <li>Securely store and share legal documents</li>
          </ul>
          <p>...NyaySetuAI can help you—<strong>for free, in seconds, from anywhere</strong>.</p>

          <h3>Who Can Use It?</h3>
          <p>NyaySetuAI is built for everyone:</p>
          <ul>
            <li><strong>Citizens</strong> seeking legal advice or help with legal procedures</li>
            <li><strong>Students</strong> learning about Indian laws and legal systems</li>
            <li><strong>Small businesses</strong> needing legal document templates</li>
            <li><strong>NGOs and activists</strong> working on legal awareness</li>
            <li><strong>Rural communities</strong> with limited access to legal services</li>
          </ul>
        `,
      },
      {
        id: "vision-mission",
        title: "Vision & Mission",
        content: `
          <h2>Vision & Mission</h2>
          
          <h3>Our Vision</h3>
          <blockquote>
            <p><strong>"To democratize legal knowledge and make justice accessible to every citizen of India, regardless of their economic status, location, or education level."</strong></p>
          </blockquote>
          <p>We envision a future where:</p>
          <ul>
            <li>Every Indian citizen understands their legal rights</li>
            <li>Legal help is available instantly, 24/7, for free</li>
            <li>Complex legal procedures are simplified through technology</li>
            <li>Language and literacy are not barriers to accessing justice</li>
          </ul>

          <h3>Our Mission</h3>
          <p>Our mission is to build an <strong>AI-powered legal assistant</strong> that:</p>
          <ul>
            <li><strong>Simplifies Legal Language:</strong> Converts complex legal jargon into simple, everyday language that anyone can understand</li>
            <li><strong>Provides Instant Answers:</strong> Uses AI to answer legal questions in real-time</li>
            <li><strong>Automates Document Drafting:</strong> Helps users create legal documents without needing a lawyer</li>
            <li><strong>Ensures Security & Privacy:</strong> Protects user data using advanced blockchain technology</li>
            <li><strong>Promotes Legal Awareness:</strong> Educates citizens about their rights and legal procedures</li>
          </ul>

          <h3>Core Values</h3>
          <ul>
            <li><strong>Accessibility:</strong> Free and easy to use for everyone</li>
            <li><strong>Accuracy:</strong> Reliable legal information backed by AI and verified legal data</li>
            <li><strong>Transparency:</strong> Clear explanations of how the system works</li>
            <li><strong>Privacy:</strong> User data is protected and never shared without consent</li>
            <li><strong>Inclusiveness:</strong> Designed for users of all backgrounds and education levels</li>
          </ul>
        `,
      },
      {
        id: "problem-statement",
        title: "Problem Statement",
        content: `
          <h2>Problem Statement</h2>
          <p>India's legal system faces significant accessibility challenges that prevent ordinary citizens from accessing justice:</p>

          <h3>1. High Cost of Legal Services</h3>
          <p>Even for simple legal matters, hiring a lawyer can cost thousands of rupees—an amount that many citizens, especially in rural areas, cannot afford. This creates a situation where:</p>
          <ul>
            <li>Poor and middle-class citizens avoid seeking legal help</li>
            <li>Small disputes remain unresolved</li>
            <li>People accept injustice due to cost constraints</li>
          </ul>

          <h3>2. Complex Legal Language</h3>
          <p>Legal documents and procedures use terminology that most people don't understand:</p>
          <ul>
            <li>IPC sections written in legal jargon</li>
            <li>Court procedures explained in complex language</li>
            <li>Legal rights hidden behind difficult terminology</li>
          </ul>
          <p><strong>Result:</strong> Citizens don't know their rights or how to exercise them.</p>

          <h3>3. Limited Access to Legal Professionals</h3>
          <p>Many areas in India, especially rural regions, have very few lawyers or legal aid centers:</p>
          <ul>
            <li>Long distances to reach a legal consultant</li>
            <li>Limited availability of lawyers in small towns</li>
            <li>Time-consuming process to get legal advice</li>
          </ul>

          <h3>4. Lack of Legal Awareness</h3>
          <p>Most citizens don't know:</p>
          <ul>
            <li>Which laws apply to their situation</li>
            <li>How to file complaints or legal applications</li>
            <li>What documents are needed for legal procedures</li>
            <li>Their fundamental legal rights</li>
          </ul>

          <h3>5. Slow and Inefficient Processes</h3>
          <p>Traditional legal processes are slow:</p>
          <ul>
            <li>Waiting days or weeks for a consultation</li>
            <li>Multiple visits to lawyers or courts</li>
            <li>Lengthy document preparation</li>
          </ul>

          <h3>How NyaySetuAI Addresses These Problems</h3>
          <table>
            <thead>
              <tr>
                <th>Problem</th>
                <th>NyaySetuAI Solution</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>High Cost</td>
                <td>100% free legal assistance powered by AI</td>
              </tr>
              <tr>
                <td>Complex Language</td>
                <td>Converts legal terms into simple, everyday language</td>
              </tr>
              <tr>
                <td>Limited Access</td>
                <td>Available 24/7 from anywhere with internet</td>
              </tr>
              <tr>
                <td>Lack of Awareness</td>
                <td>Educates users about relevant laws and procedures</td>
              </tr>
              <tr>
                <td>Slow Process</td>
                <td>Instant AI-powered responses and document generation</td>
              </tr>
            </tbody>
          </table>
        `,
      },
      {
        id: "why-nyaysetuai",
        title: "Why NyaySetuAI is Needed",
        content: `
          <h2>Why NyaySetuAI is Needed</h2>
          
          <h3>The Justice Gap in India</h3>
          <p>India has a <strong>massive justice gap</strong>—millions of people need legal help but can't access it. Consider these facts:</p>
          <ul>
            <li><strong>Lawyer-to-Population Ratio:</strong> India has only about 15 lawyers per 10,000 people</li>
            <li><strong>Pending Cases:</strong> Over 4 crore (40 million) cases pending in Indian courts</li>
            <li><strong>Rural Access:</strong> 65% of India lives in rural areas where legal services are scarce</li>
            <li><strong>Legal Aid:</strong> Government legal aid reaches less than 10% of those who need it</li>
          </ul>

          <h3>Real-World Scenarios</h3>
          
          <h4>Scenario 1: The Student Facing Harassment</h4>
          <p>A college student faces ragging but doesn't know which IPC sections apply or how to file a complaint. With NyaySetuAI:</p>
          <ul>
            <li>Ask the AI chatbot about ragging laws</li>
            <li>Get relevant IPC sections (e.g., <code>506</code>, <code>509</code>)</li>
            <li>Generate an FIR draft instantly</li>
            <li>Understand the legal procedure in simple language</li>
          </ul>

          <h4>Scenario 2: The Small Shopkeeper</h4>
          <p>A shopkeeper needs to file an RTI application to get information from a government office but doesn't know the format. With NyaySetuAI:</p>
          <ul>
            <li>Use the RTI generator tool</li>
            <li>Fill in simple details</li>
            <li>Get a properly formatted RTI application</li>
            <li>Download and submit it immediately</li>
          </ul>

          <h4>Scenario 3: The Rural Farmer</h4>
          <p>A farmer wants to know about land rights but lives 50km from the nearest lawyer. With NyaySetuAI:</p>
          <ul>
            <li>Access the platform from any smartphone</li>
            <li>Ask questions in simple language</li>
            <li>Get explanations without traveling</li>
            <li>Save documents securely on blockchain</li>
          </ul>

          <h3>Social Impact</h3>
          <p>NyaySetuAI creates measurable social change:</p>
          <ul>
            <li><strong>Empowerment:</strong> Citizens understand their rights and can take action</li>
            <li><strong>Cost Savings:</strong> Saves thousands of rupees in legal consultation fees</li>
            <li><strong>Time Efficiency:</strong> Get help in minutes instead of days</li>
            <li><strong>Rural Reach:</strong> Brings legal services to remote areas</li>
            <li><strong>Education:</strong> Builds general legal awareness in society</li>
          </ul>

          <div style="background: rgba(59, 130, 246, 0.1); border-left: 3px solid #3b82f6; padding: 1rem; margin: 1.5rem 0;">
            <p style="margin: 0;"><strong>Important:</strong> NyaySetuAI is not meant to replace lawyers. Instead, it helps with basic legal queries, prepares users for lawyer consultations, and educates people on when they actually need professional legal help.</p>
          </div>
        `,
      },
      {
        id: "target-users",
        title: "Target Users",
        content: `
          <h2>Target Users</h2>
          <p>NyaySetuAI is designed to serve a wide range of users across India:</p>

          <h3>1. General Citizens</h3>
          <p><strong>Who they are:</strong> Everyday people facing legal questions or needing legal assistance</p>
          <p><strong>Their needs:</strong></p>
          <ul>
            <li>Understanding IPC sections for incidents they experienced</li>
            <li>Filing FIRs for crimes like theft, fraud, harassment</li>
            <li>Generating legal notices for disputes</li>
            <li>Learning about their legal rights</li>
          </ul>
          <p><strong>How NyaySetuAI helps:</strong> Provides instant, simple explanations and document generation without legal jargon</p>

          <h3>2. Students</h3>
          <p><strong>Who they are:</strong> Law students, social science students, or anyone studying Indian legal systems</p>
          <p><strong>Their needs:</strong></p>
          <ul>
            <li>Learning about IPC sections and their applications</li>
            <li>Understanding legal procedures and workflows</li>
            <li>Researching case studies and legal precedents</li>
            <li>Practice drafting legal documents</li>
          </ul>
          <p><strong>How NyaySetuAI helps:</strong> Serves as an educational tool with clear explanations and examples</p>

          <h3>3. Rural Communities</h3>
          <p><strong>Who they are:</strong> People living in villages and small towns with limited access to legal services</p>
          <p><strong>Their needs:</strong></p>
          <ul>
            <li>Basic legal advice without traveling long distances</li>
            <li>Understanding land rights and agricultural laws</li>
            <li>Filing RTI applications for government transparency</li>
            <li>Protection from legal exploitation</li>
          </ul>
          <p><strong>How NyaySetuAI helps:</strong> Mobile-friendly platform accessible from anywhere with internet</p>

          <h3>4. Small Business Owners</h3>
          <p><strong>Who they are:</strong> Entrepreneurs, shopkeepers, and small business operators</p>
          <p><strong>Their needs:</strong></p>
          <ul>
            <li>Legal notices for payment recovery</li>
            <li>Understanding business-related laws</li>
            <li>Contract templates and legal agreements</li>
            <li>Consumer protection laws</li>
          </ul>
          <p><strong>How NyaySetuAI helps:</strong> Quick document generation at zero cost</p>

          <h3>5. NGOs and Social Workers</h3>
          <p><strong>Who they are:</strong> Organizations working on legal awareness and social justice</p>
          <p><strong>Their needs:</strong></p>
          <ul>
            <li>Helping beneficiaries understand their rights</li>
            <li>Generating legal documents for victims of injustice</li>
            <li>Conducting legal literacy programs</li>
            <li>Accessing legal information quickly</li>
          </ul>
          <p><strong>How NyaySetuAI helps:</strong> Scalable tool to serve multiple beneficiaries without costly legal consultations</p>

          <h3>6. Women and Marginalized Groups</h3>
          <p><strong>Who they are:</strong> Groups facing specific legal challenges due to social or economic factors</p>
          <p><strong>Their needs:</strong></p>
          <ul>
            <li>Knowledge of protection laws (domestic violence, dowry, harassment)</li>
            <li>Safe and private access to legal information</li>
            <li>Empowerment through legal awareness</li>
            <li>Help with filing complaints</li>
          </ul>
          <p><strong>How NyaySetuAI helps:</strong> Confidential, judgment-free legal assistance available 24/7</p>

          <h3>7. Participants of Government Schemes</h3>
          <p><strong>Who they are:</strong> Citizens applying for or using government benefits and services</p>
          <p><strong>Their needs:</strong></p>
          <ul>
            <li>Filing RTI applications to track scheme benefits</li>
            <li>Understanding eligibility criteria</li>
            <li>Raising complaints about denied services</li>
          </ul>
          <p><strong>How NyaySetuAI helps:</strong> RTI application generator and guidance on government procedures</p>

          <h3>User Accessibility Features</h3>
          <ul>
            <li><strong>No Legal Background Required:</strong> Designed for users with zero legal knowledge</li>
            <li><strong>Simple Language:</strong> All content in easy-to-understand terms</li>
            <li><strong>Voice Input:</strong> For users with limited literacy</li>
            <li><strong>Mobile-First:</strong> Works on smartphones, not just computers</li>
            <li><strong>Free Access:</strong> No subscription or payment required</li>
          </ul>
        `,
      },
      {
        id: "key-benefits",
        title: "Key Benefits",
        content: `
          <h2>Key Benefits</h2>
          <p>NyaySetuAI delivers tangible benefits to users and society:</p>

          <h3>For Individual Users</h3>
          
          <h4>1. Cost Savings</h4>
          <ul>
            <li><strong>Save ₹500-₹5,000</strong> per legal consultation</li>
            <li><strong>Free document drafting</strong> (typically costs ₹1,000-₹10,000)</li>
            <li><strong>Zero subscription fees</strong> or hidden charges</li>
          </ul>
          <p><em>Real Impact:</em> A user filing an RTI application and legal notice would save ₹3,000-₹8,000.</p>

          <h4>2. Time Efficiency</h4>
          <ul>
            <li><strong>Instant responses</strong> instead of waiting days for appointments</li>
            <li><strong>24/7 availability</strong>—no office hours or holidays</li>
            <li><strong>Generate documents in minutes</strong> instead of weeks</li>
          </ul>

          <h4>3. Convenience</h4>
          <ul>
            <li>Access from home—<strong>no travel required</strong></li>
            <li>Use on <strong>mobile, tablet, or computer</strong></li>
            <li>Available in <strong>any location</strong> with internet</li>
          </ul>

          <h4>4. Empowerment</h4>
          <ul>
            <li>Understand your <strong>legal rights</strong> clearly</li>
            <li><strong>Make informed decisions</strong> about legal actions</li>
            <li>Gain <strong>confidence</strong> when dealing with legal matters</li>
          </ul>

          <h3>For Society</h3>

          <h4>1. Increased Legal Awareness</h4>
          <ul>
            <li>More citizens understand laws and their rights</li>
            <li>Reduced exploitation due to legal ignorance</li>
            <li>Informed citizenry strengthens democracy</li>
          </ul>

          <h4>2. Access to Justice</h4>
          <ul>
            <li>Bridges the gap between legal system and citizens</li>
            <li>Reaches underserved rural and remote areas</li>
            <li>Enables marginalized groups to seek legal help</li>
          </ul>

          <h4>3. Reduced Burden on Legal System</h4>
          <ul>
            <li>Better-prepared citizens reduce unnecessary court visits</li>
            <li>Properly drafted documents save court time</li>
            <li>Early legal awareness prevents many disputes</li>
          </ul>

          <h4>4. Economic Impact</h4>
          <ul>
            <li>Small businesses can handle legal matters affordably</li>
            <li>Citizens save money for productive use</li>
            <li>Faster dispute resolution supports economic activity</li>
          </ul>

          <h3>For Government and Public Institutions</h3>

          <h4>1. Support for Legal Aid Programs</h4>
          <ul>
            <li>Complements government legal aid services</li>
            <li>Scales legal assistance without additional manpower</li>
            <li>Reduces cost per beneficiary</li>
          </ul>

          <h4>2. Transparent Governance</h4>
          <ul>
            <li>Easy RTI filing increases government transparency</li>
            <li>Citizens can hold authorities accountable</li>
            <li>Promotes clean and responsive administration</li>
          </ul>

          <h4>3. Data-Driven Policy Making</h4>
          <ul>
            <li>Insights on most-searched legal topics</li>
            <li>Understanding citizen legal needs</li>
            <li>Identifying gaps in legal awareness</li>
          </ul>

          <h3>Unique Technology Benefits</h3>

          <h4>1. AI-Powered Accuracy</h4>
          <ul>
            <li>Trained on vast legal datasets</li>
            <li>Continuously improving through machine learning</li>
            <li>Reliable IPC section predictions</li>
          </ul>

          <h4>2. Blockchain Security</h4>
          <ul>
            <li>Documents stored securely and cannot be tampered with</li>
            <li>Verifiable proof of document creation time</li>
            <li>Controlled sharing with specific users</li>
          </ul>

          <h4>3. Multilingual Capability (Future)</h4>
          <ul>
            <li>Will support multiple Indian languages</li>
            <li>Voice input in regional languages</li>
            <li>Truly inclusive platform for all Indians</li>
          </ul>

          <h3>Measurable Outcomes</h3>
          <table>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Impact</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Cost Reduction</td>
                <td>Up to 90% savings on legal consultations</td>
              </tr>
              <tr>
                <td>Time Savings</td>
                <td>From days/weeks to minutes</td>
              </tr>
              <tr>
                <td>Accessibility</td>
                <td>24/7 availability vs. limited office hours</td>
              </tr>
              <tr>
                <td>Reach</td>
                <td>Any location with internet vs. physical proximity</td>
              </tr>
              <tr>
                <td>User Satisfaction</td>
                <td>Simple, clear explanations vs. legal jargon</td>
              </tr>
            </tbody>
          </table>
        `,
      },
    ],
  },

  // 2. PLATFORM OVERVIEW
  {
    id: "platform-overview",
    title: "Platform Overview",
    pages: [
      {
        id: "how-nyaysetuai-works",
        title: "How NyaySetuAI Works",
        content: `
          <h2>How NyaySetuAI Works</h2>
          <p>NyaySetuAI uses <strong>artificial intelligence</strong> to understand your legal questions and provide accurate, helpful responses. Here's how the system works:</p>

          <h3>Step-by-Step Flow</h3>
          
          <h4>Step 1: User Input</h4>
          <p>You can interact with NyaySetuAI in three ways:</p>
          <ul>
            <li><strong>Text:</strong> Type your question or describe your situation in the chatbot</li>
            <li><strong>Voice:</strong> Speak your query using voice input</li>
            <li><strong>Document:</strong> Upload documents for analysis or reference</li>
          </ul>

          <h4>Step 2: AI Processing</h4>
          <p>When you submit your query:</p>
          <ol>
            <li><strong>Natural Language Understanding:</strong> The AI reads and understands your question, even if it's in simple, everyday language</li>
            <li><strong>Context Analysis:</strong> The system identifies key legal concepts, facts, and entities</li>
            <li><strong>Legal Knowledge Retrieval:</strong> The AI searches through vast legal databases for relevant laws, IPC sections, and procedures</li>
            <li><strong>Reasoning:</strong> The AI applies legal logic to your specific situation</li>
          </ol>

          <h4>Step 3: Response Generation</h4>
          <p>The AI creates a response that:</p>
          <ul>
            <li>Answers your question clearly</li>
            <li>Identifies applicable IPC sections</li>
            <li>Explains legal concepts in simple language</li>
            <li>Suggests next steps you can take</li>
          </ul>

          <h4>Step 4: User Action</h4>
          <p>Based on the AI's response, you can:</p>
          <ul>
            <li>Ask follow-up questions</li>
            <li>Generate legal documents (FIR, RTI, etc.)</li>
            <li>Save information securely</li>
            <li>Share documents with others</li>
          </ul>

          <h3>Example Workflow</h3>
          <p><strong>User Question:</strong> "My neighbor's dog bit me. What can I do legally?"</p>
          
          <p><strong>AI Processing:</strong></p>
          <ul>
            <li>Identifies incident: Animal attack causing injury</li>
            <li>Searches legal database: IPC sections related to negligence and injury</li>
            <li>Retrieves context: Previous cases of dog bite incidents</li>
          </ul>

          <p><strong>AI Response:</strong></p>
          <blockquote>
            <p>"A dog bite can be addressed under <strong>IPC Section 289</strong> (negligence with animal) and <strong>IPC Section 337/338</strong> (causing hurt). You can: 1) File an FIR at the local police station, 2) Seek medical treatment and keep bills, 3) Request compensation from the owner. Would you like me to help you draft an FIR?"</p>
          </blockquote>

          <p><strong>User Action:</strong> Click "Generate FIR" → Fill in details → Download document</p>

          <h3>Behind-the-Scenes Technology</h3>
          <ul>
            <li><strong>Large Language Models (LLM):</strong> Trained on legal texts to understand and generate legal content</li>
            <li><strong>Vector Databases:</strong> Store legal knowledge in a format AI can search quickly</li>
            <li><strong>Retrieval-Augmented Generation (RAG):</strong> Combines stored legal knowledge with AI reasoning</li>
            <li><strong>Blockchain:</strong> Ensures documents are stored securely and cannot be altered</li>
          </ul>

          <h3>What Makes It Different from Google Search?</h3>
          <table>
            <thead>
              <tr>
                <th>Google Search</th>
                <th>NyaySetuAI</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Shows links to articles and websites</td>
                <td>Provides direct, specific answers</td>
              </tr>
              <tr>
                <td>You must read and interpret legal text yourself</td>
                <td>AI simplifies and explains in plain language</td>
              </tr>
              <tr>
                <td>General information</td>
                <td>Personalized to your specific situation</td>
              </tr>
              <tr>
                <td>No document generation</td>
                <td>Creates legal documents for you</td>
              </tr>
              <tr>
                <td>No memory of previous questions</td>
                <td>Remembers conversation context</td>
              </tr>
            </tbody>
          </table>

          <h3>System Reliability</h3>
          <p>NyaySetuAI ensures reliability through:</p>
          <ul>
            <li><strong>Verified Legal Data:</strong> Trained on official IPC texts and legal databases</li>
            <li><strong>Continuous Updates:</strong> Legal knowledge base is regularly updated</li>
            <li><strong>Accuracy Checks:</strong> AI responses are validated against legal standards</li>
            <li><strong>Human-in-the-Loop:</strong> Complex cases include disclaimers to consult a lawyer</li>
          </ul>
        `,
      },
      {
        id: "interaction-types",
        title: "Supported Interaction Types",
        content: `
          <h2>Supported Interaction Types</h2>
          <p>NyaySetuAI supports multiple ways to interact with the platform, making it accessible to users with different preferences and abilities:</p>

          <h3>1. Text-Based Interaction</h3>
          <p><strong>What it is:</strong> Type your questions or commands in the chatbot interface</p>
          
          <p><strong>How to use:</strong></p>
          <ol>
            <li>Go to the Chatbot page</li>
            <li>Type your question in the text box</li>
            <li>Press Enter or click Send</li>
            <li>Read the AI's response</li>
          </ol>

          <p><strong>Best for:</strong></p>
          <ul>
            <li>Detailed queries that require specific information</li>
            <li>When you want to copy-paste text</li>
            <li>Environments where speaking is not possible</li>
          </ul>

          <p><strong>Example Questions:</strong></p>
          <ul>
            <li>"What is IPC Section 420?"</li>
            <li>"How do I file an RTI application?"</li>
            <li>"My landlord is not returning my security deposit. What can I do?"</li>
          </ul>

          <h3>2. Voice-Based Interaction</h3>
          <p><strong>What it is:</strong> Speak your questions and listen to spoken responses</p>
          
          <p><strong>How to use:</strong></p>
          <ol>
            <li>Click the microphone icon in the chatbot</li>
            <li>Speak your question clearly</li>
            <li>The system converts your speech to text</li>
            <li>AI processes and generates a written response</li>
            <li>Optionally, enable text-to-speech to hear the response</li>
          </ol>

          <p><strong>Best for:</strong></p>
          <ul>
            <li>Users with low literacy levels</li>
            <li>Hands-free operation (e.g., while driving or working)</li>
            <li>Faster input than typing</li>
            <li>Users more comfortable speaking than writing</li>
          </ul>

          <p><strong>Technology Used:</strong></p>
          <ul>
            <li><strong>Speech-to-Text (STT):</strong> Converts your voice into text the AI can understand</li>
            <li><strong>Text-to-Speech (TTS):</strong> Reads the AI's response aloud to you</li>
            <li><strong>Language Support:</strong> Currently supports Hindi and English audio</li>
          </ul>

          <h3>3. Document-Based Interaction</h3>
          <p><strong>What it is:</strong> Upload documents for the AI to analyze, reference, or store securely</p>
          
          <p><strong>Supported Document Types:</strong></p>
          <ul>
            <li><strong>PDF:</strong> Legal notices, contracts, FIRs</li>
            <li><strong>Images (JPG, PNG):</strong> Scanned documents, screenshots of legal texts</li>
            <li><strong>Text Files:</strong> Written complaints, narratives</li>
          </ul>

          <p><strong>Use Cases:</strong></p>
          <ol>
            <li><strong>Document Analysis:</strong>
              <ul>
                <li>Upload a legal notice you received</li>
                <li>AI explains what it means in simple language</li>
                <li>Suggests how to respond</li>
              </ul>
            </li>
            <li><strong>Secure Storage:</strong>
              <ul>
                <li>Upload important legal documents</li>
                <li>Store them securely on blockchain</li>
                <li>Access them anytime from anywhere</li>
              </ul>
            </li>
            <li><strong>Document Sharing:</strong>
              <ul>
                <li>Share specific documents with others using their User ID</li>
                <li>Maintain a tamper-proof record of when documents were created/shared</li>
              </ul>
            </li>
          </ol>

          <p><strong>How to Upload:</strong></p>
          <ol>
            <li>Go to "Your Uploads" page (Blockchain section)</li>
            <li>Click "Upload Document"</li>
            <li>Select file from your device</li>
            <li>Add description (optional)</li>
            <li>Click "Submit"</li>
            <li>Document is encrypted and stored on blockchain</li>
          </ol>

          <h3>4. Conversational Interaction</h3>
          <p><strong>What it is:</strong> Have a back-and-forth conversation with the AI, like chatting with a legal assistant</p>
          
          <p><strong>Features:</strong></p>
          <ul>
            <li><strong>Context Awareness:</strong> AI remembers previous messages in the conversation</li>
            <li><strong>Follow-up Questions:</strong> Ask clarifying questions without repeating information</li>
            <li><strong>Multi-turn Dialogue:</strong> Build on previous answers to explore a legal topic deeply</li>
          </ul>

          <p><strong>Example Conversation:</strong></p>
          <blockquote>
            <p><strong>You:</strong> "What is cheating under IPC?"<br>
            <strong>AI:</strong> "Cheating is defined under IPC Section 415. It involves deceiving someone to gain an unfair advantage..."<br>
            <strong>You:</strong> "What is the punishment?"<br>
            <strong>AI:</strong> "Under Section 420, cheating can lead to imprisonment up to 7 years and a fine..."<br>
            <strong>You:</strong> "Can I file a case if someone cheated me of ₹10,000?"<br>
            <strong>AI:</strong> "Yes, you can file an FIR. Would you like me to help you draft one?"</p>
          </blockquote>

          <h3>Choosing the Right Interaction Type</h3>
          <table>
            <thead>
              <tr>
                <th>Your Need</th>
                <th>Best Interaction Type</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Quick question about a law</td>
                <td>Text or Voice</td>
              </tr>
              <tr>
                <td>Understanding a document you received</td>
                <td>Document Upload + Text</td>
              </tr>
              <tr>
                <td>Generating legal documents</td>
                <td>Text (for form fields)</td>
              </tr>
              <tr>
                <td>Low literacy or prefer speaking</td>
                <td>Voice</td>
              </tr>
              <tr>
                <td>Deep research on a legal topic</td>
                <td>Conversational Text</td>
              </tr>
              <tr>
                <td>Securely storing legal records</td>
                <td>Document Upload to Blockchain</td>
              </tr>
            </tbody>
          </table>
        `,
      },
      {
        id: "supported-legal-domains",
        title: "Supported Legal Domains",
        content: `
          <h2>Supported Legal Domains</h2>
          <p>NyaySetuAI covers a wide range of legal areas relevant to everyday citizens. Here are the primary legal domains the platform supports:</p>

          <h3>1. Criminal Law (Indian Penal Code - IPC)</h3>
          <p><strong>What it covers:</strong> Crimes, offenses, and punishments under Indian law</p>
          
          <p><strong>Supported IPC Sections:</strong></p>
          <ul>
            <li><strong>Section 302:</strong> Murder</li>
            <li><strong>Section 304:</strong> Culpable homicide not amounting to murder</li>
            <li><strong>Section 307:</strong> Attempt to murder</li>
            <li><strong>Section 323:</strong> Voluntarily causing hurt</li>
            <li><strong>Section 354:</strong> Assault or criminal force on woman</li>
            <li><strong>Section 376:</strong> Rape</li>
            <li><strong>Section 379:</strong> Theft</li>
            <li><strong>Section 406:</strong> Criminal breach of trust</li>
            <li><strong>Section 420:</strong> Cheating</li>
            <li><strong>Section 498A:</strong> Cruelty to married woman</li>
            <li><strong>Section 500:</strong> Defamation</li>
            <li><strong>Section 506:</strong> Criminal intimidation</li>
            <li>...and 100+ more IPC sections</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Predict which IPC sections apply to your incident</li>
            <li>Explain what each section means in simple language</li>
            <li>Tell you the punishment/penalties</li>
            <li>Help draft FIRs for criminal complaints</li>
          </ul>

          <h3>2. Civil Law</h3>
          <p><strong>What it covers:</strong> Disputes between individuals or organizations (not criminal)</p>
          
          <p><strong>Supported Topics:</strong></p>
          <ul>
            <li><strong>Property Disputes:</strong> Land ownership, boundary issues, encroachment</li>
            <li><strong>Contract Law:</strong> Breach of contract, agreements</li>
            <li><strong>Family Law:</strong> Marriage, divorce, child custody, maintenance</li>
            <li><strong>Consumer Protection:</strong> Defective products, unfair trade practices</li>
            <li><strong>Defamation:</strong> False statements damaging reputation</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Explain your civil rights</li>
            <li>Draft legal notices for civil disputes</li>
            <li>Guide you on when to file a civil suit</li>
          </ul>

          <h3>3. Right to Information (RTI)</h3>
          <p><strong>What it covers:</strong> Citizens' right to access government information</p>
          
          <p><strong>Supported Activities:</strong></p>
          <ul>
            <li>Filing RTI applications</li>
            <li>Understanding RTI Act, 2005</li>
            <li>Knowing what information can/cannot be requested</li>
            <li>Complaint procedures if RTI is denied</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Automated RTI application generator</li>
            <li>Templates for different types of RTI requests</li>
            <li>Guidance on fees and procedures</li>
          </ul>

          <h3>4. Bail Applications</h3>
          <p><strong>What it covers:</strong> Applying for temporary release from custody</p>
          
          <p><strong>Supported Types:</strong></p>
          <ul>
            <li><strong>Regular Bail:</strong> For less serious offenses</li>
            <li><strong>Anticipatory Bail:</strong> Before arrest when arrest is anticipated</li>
            <li><strong>Interim Bail:</strong> Temporary bail for urgent matters</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Generate bail application drafts</li>
            <li>Explain eligibility criteria</li>
            <li>Suggest grounds for bail based on your case</li>
          </ul>

          <h3>5. Consumer Rights</h3>
          <p><strong>What it covers:</strong> Protection of consumers from unfair business practices</p>
          
          <p><strong>Supported Issues:</strong></p>
          <ul>
            <li>Defective products</li>
            <li>Wrong billing</li>
            <li>False advertising</li>
            <li>Poor service quality</li>
            <li>Warranty/guarantee claims</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Draft consumer complaint letters</li>
            <li>Explain Consumer Protection Act</li>
            <li>Guide on filing complaints with Consumer Forum</li>
          </ul>

          <h3>6. Labour and Employment Law</h3>
          <p><strong>What it covers:</strong> Rights of workers and employees</p>
          
          <p><strong>Supported Topics:</strong></p>
          <ul>
            <li>Wrongful termination</li>
            <li>Non-payment of wages</li>
            <li>Workplace harassment</li>
            <li>Maternity benefits</li>
            <li>Provident fund issues</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Explain employee rights</li>
            <li>Draft legal notices to employers</li>
            <li>Guide on labor court procedures</li>
          </ul>

          <h3>7. Cyber Crimes</h3>
          <p><strong>What it covers:</strong> Crimes committed using computers, internet, or digital devices</p>
          
          <p><strong>Supported Offenses:</strong></p>
          <ul>
            <li>Online harassment/cyberbullying</li>
            <li>Identity theft</li>
            <li>Online fraud/phishing</li>
            <li>Revenge porn</li>
            <li>Hacking</li>
          </ul>

          <p><strong>Relevant Laws:</strong></p>
          <ul>
            <li>IT Act, 2000</li>
            <li>IPC sections applicable to cyber crimes (Sections 419, 420, 463, 465, 469, 500, 501, 506)</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Identify applicable cyber crime laws</li>
            <li>Draft cyber crime FIRs</li>
            <li>Explain how to report to Cyber Cell</li>
          </ul>

          <h3>8. Women and Child Protection</h3>
          <p><strong>What it covers:</strong> Special laws protecting women and children</p>
          
          <p><strong>Supported Laws:</strong></p>
          <ul>
            <li><strong>Protection of Women from Domestic Violence Act (PWDVA):</strong> Domestic abuse protection</li>
            <li><strong>Dowry Prohibition Act:</strong> Cases involving dowry demands or harassment</li>
            <li><strong>POCSO Act:</strong> Protection of children from sexual offenses</li>
            <li><strong>Sexual Harassment at Workplace:</strong> Vishakha Guidelines and Prevention of Sexual Harassment Act</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Explain these special protection laws</li>
            <li>Draft FIRs for domestic violence, dowry harassment</li>
            <li>Guide on filing complaints with Women's Commission</li>
          </ul>

          <h3>9. Land and Property Law</h3>
          <p><strong>What it covers:</strong> Legal issues related to land, houses, and property</p>
          
          <p><strong>Supported Topics:</strong></p>
          <ul>
            <li>Property ownership disputes</li>
            <li>Tenancy and rent issues</li>
            <li>Illegal possession/encroachment</li>
            <li>Property document verification</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Explain property rights</li>
            <li>Draft legal notices for landlord-tenant disputes</li>
            <li>Guide on property litigation</li>
          </ul>

          <h3>10. Traffic and Motor Vehicle Laws</h3>
          <p><strong>What it covers:</strong> Road traffic violations and vehicle-related legal issues</p>
          
          <p><strong>Supported Topics:</strong></p>
          <ul>
            <li>Traffic fines and penalties</li>
            <li>Vehicle theft (IPC Section 379)</li>
            <li>Accident claims</li>
            <li>Driving license issues</li>
          </ul>

          <p><strong>How NyaySetuAI helps:</strong></p>
          <ul>
            <li>Explain Motor Vehicles Act violations</li>
            <li>Draft FIRs for vehicle theft or accident cases</li>
          </ul>

          <h3>Future Expansions (Coming Soon)</h3>
          <ul>
            <li><strong>Intellectual Property:</strong> Copyright, trademark, patent</li>
            <li><strong>Banking and Financial Law:</strong> Loan disputes, fraud</li>
            <li><strong>Environmental Law:</strong> Pollution, conservation</li>
            <li><strong>State-Specific Laws:</strong> Laws unique to different Indian states</li>
            <li><strong>Local Language Support:</strong> Regional language interpretation of laws</li>
          </ul>

          <h3>Limitations</h3>
          <p>NyaySetuAI does not currently support:</p>
          <ul>
            <li>International law or cross-border legal issues</li>
            <li>Highly specialized legal fields (e.g., maritime law, aviation law)</li>
            <li>Legal representation in court (the platform is for information only)</li>
          </ul>

          <p><strong>Disclaimer:</strong> NyaySetuAI provides legal information, not legal advice. For complex or serious legal matters, always consult a qualified lawyer.</p>
        `,
      },
      {
        id: "accessibility-inclusiveness",
        title: "Accessibility & Inclusiveness",
        content: `
          <h2>Accessibility & Inclusiveness</h2>
          <p>NyaySetuAI is designed to be accessible to <strong>all citizens</strong>, regardless of their background, education, location, or abilities. Here's how we ensure inclusiveness:</p>

          <h3>1. Simple Language</h3>
          <p><strong>Challenge:</strong> Legal documents are full of jargon that ordinary people don't understand.</p>
          <p><strong>Our Solution:</strong></p>
          <ul>
            <li>AI converts complex legal terms into <strong>simple, everyday language</strong></li>
            <li>Explanations use examples and analogies</li>
            <li>Avoids unnecessary legal terminology</li>
          </ul>
          <p><strong>Example:</strong></p>
          <blockquote>
            <p><strong>Legal Jargon:</strong> "Cognizable offense under IPC Section 379 with punishment of imprisonment up to three years or fine or both"<br>
            <strong>NyaySetuAI Translation:</strong> "Theft is a serious crime under IPC Section 379. If proven guilty, a person can go to jail for up to 3 years, or pay a fine, or both."</p>
          </blockquote>

          <h3>2. Voice Input for Low-Literacy Users</h3>
          <p><strong>Challenge:</strong> Many citizens, especially in rural areas, have limited reading/writing skills.</p>
          <p><strong>Our Solution:</strong></p>
          <ul>
            <li><strong>Speech-to-Text:</strong> Users can speak their questions instead of typing</li>
            <li><strong>Text-to-Speech:</strong> Responses can be read aloud</li>
            <li>Supports both <strong>Hindi and English</strong> voice input</li>
          </ul>
          <p><strong>Use Case:</strong> A farmer in a village can speak into their phone to ask, "Mere khet par kabza kiya hai, kya karun?" (Someone has encroached on my field, what should I do?) and get a spoken response.</p>

          <h3>3. Mobile-First Design</h3>
          <p><strong>Challenge:</strong> Many Indians access the internet primarily through smartphones, not computers.</p>
          <p><strong>Our Solution:</strong></p>
          <ul>
            <li>Fully responsive design that works perfectly on <strong>small screens</strong></li>
            <li>Optimized for <strong>low bandwidth</strong> connections</li>
            <li>Touch-friendly buttons and interfaces</li>
            <li>Minimal data usage</li>
          </ul>
          <p><strong>Impact:</strong> Users in remote areas with slow internet can still access the platform smoothly.</p>

          <h3>4. Free and Open Access</h3>
          <p><strong>Challenge:</strong> Legal services are expensive, creating a barrier for poor and middle-class citizens.</p>
          <p><strong>Our Solution:</strong></p>
          <ul>
            <li><strong>100% free:</strong> No subscription fees, no hidden charges</li>
            <li><strong>No paywall:</strong> All features available to everyone</li>
            <li><strong>No login required for basic queries</strong> (optional login for advanced features)</li>
          </ul>

          <h3>5. Multilingual Support (Future)</h3>
          <p><strong>Challenge:</strong> India has 22 official languages, and many citizens are not comfortable with English or Hindi.</p>
          <p><strong>Planned Solution:</strong></p>
          <ul>
            <li>AI translations in <strong>regional languages</strong> (Tamil, Telugu, Bengali, Marathi, Gujarati, etc.)</li>
            <li>Voice input and output in multiple Indian languages</li>
            <li>Legal terms explained in the user's native language</li>
          </ul>
          <p><strong>Timeline:</strong> Phased rollout starting with top 5 most-spoken Indian languages</p>

          <h3>6. Dark Mode for Accessibility</h3>
          <p><strong>Challenge:</strong> Bright white screens can cause eye strain, especially for users with visual sensitivities.</p>
          <p><strong>Our Solution:</strong></p>
          <ul>
            <li><strong>Dark mode toggle:</strong> Users can switch to a dark theme</li>
            <li>Reduces eye strain during prolonged use</li>
            <li>Saves battery on OLED screens</li>
          </ul>

          <h3>7. Offline Access (Future Enhancement)</h3>
          <p><strong>Challenge:</strong> Internet connectivity is unreliable in many rural areas.</p>
          <p><strong>Planned Solution:</strong></p>
          <ul>
            <li>Downloadable database of common IPC sections and legal FAQs</li>
            <li>Offline document templates</li>
            <li>Sync when internet becomes available</li>
          </ul>

          <h3>8. Gender-Inclusive Content</h3>
          <p><strong>Approach:</strong></p>
          <ul>
            <li>Neutral language that respects all genders</li>
            <li>Specific sections on women's rights and protection laws</li>
            <li>Confidential and judgment-free assistance for sensitive issues (domestic violence, harassment)</li>
          </ul>

          <h3>9. Support for Persons with Disabilities</h3>
          <p><strong>Features:</strong></p>
          <ul>
            <li><strong>Screen reader compatibility:</strong> Works with tools like JAWS and NVDA</li>
            <li><strong>Keyboard navigation:</strong> Fully navigable without a mouse</li>
            <li><strong>High contrast mode:</strong> For users with low vision</li>
            <li><strong>Voice input:</strong> For users with mobility impairments</li>
          </ul>

          <h3>10. Cultural Sensitivity</h3>
          <p><strong>Approach:</strong></p>
          <ul>
            <li>Examples and case studies from diverse Indian contexts</li>
            <li>Awareness of regional variations in legal practices</li>
            <li>Respectful language for sensitive topics (caste, religion, gender)</li>
          </ul>

          <h3>Accessibility Checklist</h3>
          <table>
            <thead>
              <tr>
                <th>Barrier</th>
                <th>NyaySetuAI Solution</th>
                <th>Impact</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Complex language</td>
                <td>AI simplification</td>
                <td>Legal literacy for all</td>
              </tr>
              <tr>
                <td>Low literacy</td>
                <td>Voice input/output</td>
                <td>Includes millions of low-literate citizens</td>
              </tr>
              <tr>
                <td>High cost</td>
                <td>Free platform</td>
                <td>Equal access regardless of income</td>
              </tr>
              <tr>
                <td>Geographic distance</td>
                <td>Mobile-first, online</td>
                <td>Reaches remote areas</td>
              </tr>
              <tr>
                <td>Language barrier</td>
                <td>Multilingual (future)</td>
                <td>Native language support</td>
              </tr>
              <tr>
                <td>Disabilities</td>
                <td>Screen reader, voice, keyboard navigation</td>
                <td>Accessible to persons with disabilities</td>
              </tr>
            </tbody>
          </table>

          <h3>Commitment to Inclusiveness</h3>
          <p>NyaySetuAI is committed to:</p>
          <ul>
            <li><strong>Continuous improvement:</strong> Regular user feedback to identify and remove barriers</li>
            <li><strong>Community engagement:</strong> Working with NGOs and grassroots organizations</li>
            <li><strong>Education:</strong> Not just providing tools, but teaching users about their rights</li>
            <li><strong>Privacy:</strong> Ensuring marginalized users feel safe using the platform</li>
          </ul>

          <p><strong>Goal:</strong> Make legal assistance truly universal—<em>"Justice for All, Barriers for None."</em></p>
        `,
      },
    ],
  },

  //3. CORE FEATURES
  {
    id: "core-features",
    title: "Core Features",
    pages: [
      {
        id: "legal-query-assistant",
        title: "Legal Query Assistant",
        content: `
          <h2>Legal Query Assistant</h2>
          <p>The AI-powered chatbot that answers your legal questions in simple language.</p>
          
          <h3>What It Does</h3>
          <ul>
            <li>Answers questions about Indian laws, IPC sections, and legal procedures</li>
            <li>Explains complex legal concepts in simple, everyday language</li>
            <li>Provides context-aware responses based on your situation</li>
            <li>Remembers conversation history for follow-up questions</li>
          </ul>

          <h3>How to Use</h3>
          <ol>
            <li>Navigate to the <strong>AI Chatbot</strong> page</li>
            <li>Type your question in the chat box</li>
            <li>Press Enter or click Send</li>
            <li>Read the AI's response</li>
            <li>Ask follow-up questions if needed</li>
          </ol>

          <h3>Example Queries</h3>
          <ul>
            <li>"What is IPC Section 420?"</li>
            <li>"Someone stole my phone. What legal actions can I take?"</li>
            <li>"How do I file a complaint against my landlord?"</li>
            <li>"What are the penalties for drunk driving in India?"</li>
          </ul>

          <h3>Features</h3>
          <ul>
            <li><strong>24/7 Availability:</strong> Get answers anytime, day or night</li>
            <li><strong>Instant Responses:</strong> No waiting for appointments</li>
            <li><strong>Conversational:</strong> Natural dialogue like chatting with a legal expert</li>
            <li><strong>Free:</strong> Unlimited questions at no cost</li>
          </ul>
        `,
      },
      {
        id: "ipc-section-prediction",
        title: "IPC Section Prediction",
        content: `
          <h2>IPC Section Prediction</h2>
          <p>Automatically identify which IPC (Indian Penal Code) sections apply to your legal situation.</p>

          <h3>How It Works</h3>
          <ol>
            <li>Describe your incident or situation in plain language</li>
            <li>AI analyzes the description using machine learning</li>
            <li>System predicts relevant IPC sections</li>
            <li>Get explanations of what each section means</li>
            <li>Learn about applicable punishments</li>
          </ol>

          <h3>Supported Incidents</h3>
          <ul>
            <li>Theft, robbery, burglary</li>
            <li>Fraud,cheating, criminal breach of trust</li>
            <li>Assault, battery, causing hurt</li>
            <li>Harassment, stalking, intimidation</li>
            <li>Defamation, insult</li>
            <li>Property damage</li>
            <li>Cybercrimes</li>
            <li>And 100+ more scenarios</li>
          </ul>

          <h3>Example Use Case</h3>
          <p><strong>Input:</strong> "Someone posted fake information about me on Facebook to damage my reputation."</p>
          <p><strong>AI Prediction:</strong></p>
          <ul>
            <li><strong>IPC Section 500:</strong> Defamation - Making false statements to harm reputation</li>
            <li><strong>IT Act Section 66A (relevant):</strong> Sending offensive messages through communication service</li>
            <li><strong>Punishment:</strong> Imprisonment up to 2 years or fine or both</li>
          </ul>

          <h3>Accuracy</h3>
          <ul>
            <li>Trained on thousands of real legal cases</li>
            <li>Regularly updated with new legal precedents</li>
            <li>Achieves 85%+ accuracy on common crime categories</li>
          </ul>

          <h3>Navigating to IPC Prediction</h3>
          <p>Go to <strong>More → Predict IPC</strong> in the navigation</p>
        `,
      },
      {
        id: "legal-document-drafting",
        title: "Legal Document Drafting",
        content: `
          <h2>Legal Document Drafting</h2>
          <p>Automatically generate legal documents like FIRs, RTI applications, bail applications, and legal notices.</p>

          <h3>Supported Document Types</h3>
          
          <h4>1. FIR (First Information Report)</h4>
          <ul>
            <li>Formal complaint to police about a crime</li>
            <li>Used for theft, assault, fraud, etc.</li>
            <li>AI generates properly formatted FIR based on your details</li>
          </ul>

          <h4>2. RTI Application</h4>
          <ul>
            <li>Request information from government offices</li>
            <li>Based on Right to Information Act, 2005</li>
            <li>Template includes all required fields</li>
          </ul>

          <h4>3. Bail Application</h4>
          <ul>
            <li>Request temporary release from custody</li>
            <li>Includes grounds for bail</li>
            <li>Properly formatted for court submission</li>
          </ul>

          <h4>4. Legal Notice</h4>
          <ul>
            <li>Formal warning before filing a lawsuit</li>
            <li>Used for payment recovery, disputes, etc.</li>
            <li>Professional legal format</li>
          </ul>

          <h3>Document Generation Process</h3>
          <ol>
            <li>Select document type</li>
            <li>Fill in required information through simple forms</li>
            <li>AI generates document using legal templates</li>
            <li>Review and edit if needed</li>
            <li>Download as PDF</li>
            <li>Optionally save to blockchain for secure storage</li>
          </ol>

          <h3>Quality Assurance</h3>
          <ul>
            <li>Templates verified by legal experts</li>
            <li>Follows standard legal formats</li>
            <li>Automatically includes mandatory fields</li>
            <li>Checks for completeness before generation</li>
          </ul>

          <h3>Cost Savings</h3>
          <p>Hiring a lawyer to draft these documents typically costs:</p>
          <ul>
            <li><strong>FIR Draft:</strong> ₹500-₹2,000</li>
            <li><strong>Legal Notice:</strong> ₹2,000-₹10,000</li>
            <li><strong>Bail Application:</strong> ₹3,000-₹20,000</li>
          </ul>
          <p><strong>With NyaySetuAI: ₹0 (Free)</strong></p>

          <h3>Access Documents</h3>
          <p>Navigate to <strong>More → Generate Draft</strong></p>
        `,
      },
    ],
  },

  // 4. USER WORKFLOWS
  {
    id: "user-workflows",
    title: "User Workflows",
    pages: [
      {
        id: "asking-legal-question",
        title: "Asking a Legal Question",
        content: `
          <h2>Asking a Legal Question</h2>
          <p>Step-by-step guide to getting legal help through the chatbot.</p>

          <h3>Step-by-Step Process</h3>
          
          <h4>Step 1: Access the Chatbot</h4>
          <ul>
            <li>Click <strong>AI Chatbot</strong> in the navigation menu</li>
            <li>The chatbot interface opens with a welcome message</li>
          </ul>

          <h4>Step 2: Formulate Your Question</h4>
          <p><strong>Tips for good questions:</strong></p>
          <ul>
            <li>Be specific about your situation</li>
            <li>Include relevant details (what, when, where)</li>
            <li>Use simple, clear language</li>
            <li>Don't worry about legal terminology—describe in your own words</li>
          </ul>

          <p><strong>Example Good Questions:</strong></p>
          <ul>
            <li>"My employer hasn't paid my salary for 3 months. What can I do?"</li>
            <li>"Someone is spreading false rumors about me on social media. Is this illegal?"</li>
            <li>"I want to file an RTI to know the status of my ration card application. How do I do it?"</li>
          </ul>

          <h4>Step 3: Send Your Question</h4>
          <ul>
            <li>Type in the chat box</li>
            <li>Press <strong>Enter</strong> or click <strong>Send</strong></li>
            <li>Wait a few seconds for AI to process</li>
          </ul>

          <h4>Step 4: Read the Response</h4>
          <ul>
            <li>AI provides detailed answer</li>
            <li>Explains relevant laws in simple language</li>
            <li>Suggests next steps you can take</li>
          </ul>

          <h4>Step 5: Ask Follow-Up Questions</h4>
          <ul>
            <li>Clarify anything you don't understand</li>
            <li>Ask for more details</li>
            <li>Explore related topics</li>
          </ul>

          <h3>Sample Conversation</h3>
          <blockquote>
            <p><strong>You:</strong> "Someone hit my car and drove away. What should I do?"</p>
            <p><strong>AI:</strong> "This is a hit-and-run case. You should: 1) File an FIR under IPC Section 279 (rash driving) and Section 338 (causing grievous hurt), 2) Collect any evidence like CCTV footage or witness statements, 3) Inform your insurance company. Would you like help drafting an FIR?"</p>
            <p><strong>You:</strong> "Yes, help me draft an FIR"</p>
            <p><strong>AI:</strong> "I'll help you create an FIR. Please provide these details: 1) Date and time of incident, 2) Location, 3) Description of the vehicle if you remember..."</p>
          </blockquote>

          <h3>Best Practices</h3>
          <ul>
            <li><strong>Be honest:</strong> Provide accurate information</li>
            <li><strong>Be patient:</strong> Complex questions may take a few extra seconds</li>
            <li><strong>Context matters:</strong> Mention if you've already taken any action</li>
            <li><strong>Use voice input:</strong> If typing is difficult, click the microphone icon</li>
          </ul>

          <h3>What the Chatbot Can and Cannot Do</h3>
          <table>
            <thead>
              <tr>
                <th>Can Do ✓</th>
                <th>Cannot Do ✗</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Explain laws and IPC sections</td>
                <td>Represent you in court</td>
              </tr>
              <tr>
                <td>Help draft legal documents</td>
                <td>File cases on your behalf</td>
              </tr>
              <tr>
                <td>Suggest next steps to take</td>
                <td>Give personalized legal advice (consult a lawyer for this)</td>
              </tr>
              <tr>
                <td>Provide general legal information</td>
                <td>Guarantee legal outcomes</td>
              </tr>
            </tbody>
          </table>
        `,
      },
      {
        id: "generating-legal-documents",
        title: "Generating Legal Documents",
        content: `
          <h2>Generating Legal Documents</h2>
          <p>How to create FIRs, RTI applications, bail applications, and legal notices using NyaySetuAI.</p>

          <h3>Document Generation Workflow</h3>
          
          <h4>Step 1: Navigate to Generate Draft</h4>
          <ul>
            <li>Click <strong>More → Generate Draft</strong> in the navigation</li>
            <li>You'll see options for different document types</li>
          </ul>

          <h4>Step 2: Select Document Type</h4>
          <ul>
           <li><strong>FIR:</strong> To report a crime to police</li>
            <li><strong>RTI Application:</strong> To request government information</li>
            <li><strong>Bail Application:</strong> To request release from custody</li>
            <li><strong>Legal Notice:</strong> To formally warn someone before legal action</li>
          </ul>

          <h4>Step 3: Fill Required Information</h4>
          <p>Each document type has a form with specific fields. For example:</p>
          
          <p><strong>For FIR:</strong></p>
          <ul>
            <li>Your name and contact details</li>
            <li>Date, time, and place of incident</li>
            <li>Description of what happened</li>
            <li>Suspect details (if known)</li>
            <li>Type of crime/IPC sections (AI can suggest these)</li>
          </ul>

          <p><strong>For RTI Application:</strong></p>
          <ul>
            <li>Your name and address</li>
            <li>Name of government office/department</li>
            <li>Information you're requesting</li>
            <li>Reason for request (optional)</li>
          </ul>

          <h4>Step 4: Review AI-Generated Draft</h4>
          <ul>
            <li>AI creates document based on your inputs</li>
            <li>Review for accuracy and completeness</li>
            <li>Edit any section if needed</li>
          </ul>

          <h4>Step 5: Download Document</h4>
          <ul>
            <li>Click <strong>Download PDF</strong></li>
            <li>Document is saved to your device</li>
            <li>Print or email as needed</li>
          </ul>

          <h4>Step 6: (Optional) Save to Blockchain</h4>
          <ul>
            <li>Click <strong>Save to Blockchain</strong></li>
            <li>Document is securely stored with timestamp</li>
            <li>Creates tamper-proof record</li>
            <li>Can be retrieved anytime from "Your Uploads"</li>
          </ul>

          <h3>Document-Specific Guides</h3>
          
          <h4>Generating an FIR</h4>
          <ol>
            <li>Select "FIR" from document types</li>
            <li>Describe the incident in detail</li>
            <li>AI suggests applicable IPC sections</li>
            <li>Fill in suspect details if known</li>
            <li>Download and take to police station</li>
          </ol>

          <h4>Generating an RTI Application</h4>
          <ol>
            <li>Select "RTI Application"</li>
            <li>Identify the government department</li>
            <li>Clearly state what information you need</li>
            <li>AI formats it according to RTI Act requirements</li>
            <li>Download, attach fee receipt (usually ₹10), and submit</li>
          </ol>

          <h4>Generating a Legal Notice</h4>
          <ol>
            <li>Select "Legal Notice"</li>
            <li>Provide recipient's name and address</li>
            <li>Describe the issue/dispute</li>
            <li>State your demand (payment, action, etc.)</li>
            <li>AI creates formal notice with legal language</li>
            <li>Send via registered post or email</li>
          </ol>

          <h3>Quality Tips</h3>
          <ul>
            <li><strong>Be accurate:</strong> Provide correct dates, names, and facts</li>
            <li><strong>Be specific:</strong> More details = better document</li>
            <li><strong>Be truthful:</strong> False information can have legal consequences</li>
            <li><strong>Double-check:</strong> Review before finalizing</li>
          </ul>

          <h3>After Generating the Document</h3>
          <p><strong>FIR:</strong> Take printed copy to police station and request it be filed</p>
          <p><strong>RTI:</strong> Submit to Public Information Officer (PIO) of relevant department</p>
          <p><strong>Bail Application:</strong> File in appropriate court through a lawyer or yourself</p>
          <p><strong>Legal Notice:</strong> Send via registered post and keep delivery proof</p>
        `,
      },
      {
        id: "blockchain-document-management",
        title: "Uploading & Securing Documents",
        content: `
          <h2>Uploading & Securing Documents on Blockchain</h2>
          <p>Store your legal documents securely using blockchain technology for tamper-proof, permanent storage.</p>

          <h3>Why Use Blockchain Storage?</h3>
          <ul>
            <li><strong>Tamper-Proof:</strong> Once stored, documents cannot be altered or deleted</li>
            <li><strong>Timestamp Verification:</strong> Proof of when document was created</li>
            <li><strong>Decentralized:</strong> Not controlled by any single entity</li>
            <li><strong>Controlled Sharing:</strong> Share with specific people using their User ID</li>
            <li><strong>Permanent Access:</strong> Retrieve documents anytime, anywhere</li>
          </ul>

          <h3>How to Upload Documents</h3>
          
          <h4>Step 1: Navigate to Your Uploads</h4>
          <ul>
            <li>Click <strong>More → Your Uploads</strong></li>
            <li>This opens the blockchain dashboard</li>
          </ul>

          <h4>Step 2: Upload a New Document</h4>
          <ul>
            <li>Click <strong>Upload Document</strong> button</li>
            <li>Select file from your device (PDF, JPG, PNG supported)</li>
            <li>Add a description (optional but recommended)</li>
            <li>Click <strong>Submit</strong></li>
          </ul>

          <h4>Step 3: Document Processing</h4>
          <ul>
            <li>Document is encrypted for security</li>
            <li>Stored on blockchain with unique hash</li>
            <li>Timestamp recorded automatically</li>
            <li>You receive a transaction ID</li>
          </ul>

          <h3>Viewing Your Documents</h3>
          <ul>
            <li>All your uploaded documents appear in "Your Uploads"</li>
            <li>See document name, upload date, file size</li>
            <li>Click <strong>View</strong> to open document</li>
            <li>Click <strong>Download</strong> to save a copy</li>
          </ul>

          <h3>Sharing Documents Securely</h3>
          
          <h4>Why Share via Blockchain?</h4>
          <ul>
            <li>Proof that you shared the document at a specific time</li>
            <li>Recipient cannot claim they didn't receive it</li>
            <li>Creates auditable trail</li>
          </ul>

          <h4>How to Share</h4>
          <ol>
            <li>Go to "Your Uploads"</li>
            <li>Find the document you want to share</li>
            <li>Click <strong>Share</strong></li>
            <li>Enter recipient's User ID</li>
            <li>Click <strong>Confirm Share</strong></li>
            <li>Document access is granted to that user</li>
          </ol>

          <h3>Blockchain Verification</h3>
          <p>Each document gets:</p>
          <ul>
            <li><strong>Unique Hash:</strong> Digital fingerprint of the document</li>
            <li><strong>Block Number:</strong> Position in the blockchain</li>
            <li><strong>Timestamp:</strong> Exact date and time of upload</li>
            <li><strong>Transaction ID:</strong> Unique identifier for the storage event</li>
          </ul>

          <h3>Use Cases</h3>
          <ul>
            <li><strong>Legal Documents:</strong> Store FIRs, notices, contracts</li>
            <li><strong>Evidence:</strong> Photos, videos, witness statements</li>
            <li><strong>Property Papers:</strong> Sale deeds, agreements</li>
            <li><strong>Certificates:</strong> Educational, identity documents</li>
            <li><strong>Business Records:</strong> Invoices, agreements</li>
          </ul>

          <h3>Security & Privacy</h3>
          <ul>
            <li>Only you can access your documents (unless you share them)</li>
            <li>Documents are encrypted end-to-end</li>
            <li>Blockchain stores hash, not actual document content (for privacy)</li>
            <li>You control who can view each document</li>
          </ul>

          <h3>Limitations</h3>
          <ul>
            <li><strong>File Size:</strong> Maximum 10MB per document</li>
            <li><strong>File Types:</strong> PDF, JPG, PNG only</li>
            <li><strong>Permanence:</strong> Once uploaded, cannot be deleted (by design)</li>
          </ul>
        `,
      },
    ],
  },

  // 5. SECURITY & PRIVACY
  {
    id: "security-privacy",
    title: "Security & Privacy",
    pages: [
      {
        id: "data-protection",
        title: "User Data Protection",
        content: `
          <h2>User Data Protection</h2>
          <p>How NyaySetuAI protects your personal and legal information.</p>

          <h3>Data We Collect</h3>
          <ul>
            <li><strong>Account Information:</strong> Email, username (if you create an account)</li>
            <li><strong>Chat History:</strong> Your questions and AI responses</li>
            <li><strong>Documents:</strong> Files you upload to blockchain</li>
            <li><strong>Usage Data:</strong> Features you use, pages visited (for improving platform)</li>
          </ul>

          <h3>How We Protect Your Data</h3>
          
          <h4>1. Encryption</h4>
          <ul>
            <li>All data transmitted over <strong>HTTPS</strong> (encrypted connection)</li>
            <li>Documents encrypted before blockchain storage</li>
            <li>Passwords hashed using industry-standard algorithms</li>
          </ul>

          <h4>2. Access Control</h4>
          <ul>
            <li>Only you can access your documents</li>
            <li>Sharing requires explicit permission</li>
            <li>Admin team cannot read your encrypted documents</li>
          </ul>

          <h4>3. Blockchain Security</h4>
          <ul>
            <li>Decentralized storage prevents single point of failure</li>
            <li>Cryptographic hashing ensures data integrity</li>
            <li>Tamper-proof records</li>
          </ul>

          <h4>4. No Sale of Data</h4>
          <ul>
            <li><strong>We never sell your data</strong> to third parties</li>
            <li>No advertising based on your legal queries</li>
            <li>Your privacy is not monetized</li>
          </ul>

          <h3>Your Rights</h3>
          <ul>
            <li><strong>Right to Access:</strong> Request copy of all data we have about you</li>
            <li><strong>Right to Delete:</strong> Delete your account and associated data</li>
            <li><strong>Right to Correct:</strong> Update incorrect personal information</li>
            <li><strong>Right to Export:</strong> Download your data in portable format</li>
          </ul>

          <h3>What We Don't Store</h3>
          <ul>
            <li>Payment information (platform is free)</li>
            <li>Location tracking (unless explicitly needed for a feature)</li>
            <li>Device fingerprinting for advertising</li>
          </ul>

          <h3>Data Retention</h3>
          <ul>
            <li><strong>Chat History:</strong> Stored as long as you have an account</li>
            <li><strong>Blockchain Documents:</strong> Permanent (by blockchain design)</li>
            <li><strong>Usage Analytics:</strong> Anonymized after 90 days</li>
          </ul>

          <h3>Compliance</h3>
          <ul>
            <li>Complies with IT Act, 2000 (India)</li>
            <li>Follows data protection best practices</li>
            <li>Regular security audits</li>
          </ul>
        `,
      },
      {
        id: "ethical-ai",
        title: "Ethical AI Usage & Limitations",
        content: `
          <h2>Ethical AI Usage & Limitations</h2>
          
          <h3>Our Ethical Commitments</h3>
          
          <h4>1. Transparency</h4>
          <ul>
            <li>We clearly state that responses come from AI, not human lawyers</li>
            <li>Explain how the AI works and its limitations</li>
            <li>Show confidence levels when applicable</li>
          </ul>

          <h4>2. No Bias</h4>
          <ul>
            <li>AI trained on diverse, representative legal data</li>
            <li>Regular testing for gender, caste, religious bias</li>
            <li>Equal treatment of all users regardless of background</li>
          </ul>

          <h4>3. Accuracy Over Speed</h4>
          <ul>
            <li>AI designed to provide accurate information, not just fast answers</li>
            <li>Unknown questions trigger "I don't know" responses rather than guessing</li>
            <li>Regular validation against legal experts</li>
          </ul>

          <h4>4. User Empowerment, Not Replacement</h4>
          <ul>
            <li>Tool to complement, not replace, lawyers</li>
            <li>Educates users so they can make informed decisions</li>
            <li>Encourages consulting lawyers for complex cases</li>
          </ul>

          <h3>System Limitations</h3>
          
          <h4>What NyaySetuAI Can Do</h4>
          <ul>
            <li>Provide general legal information</li>
            <li>Explain IPC sections and laws</li>
            <li>Generate document templates</li>
            <li>Suggest possible legal actions</li>
          </ul>

          <h4>What NyaySetuAI Cannot Do</h4>
          <ul>
            <li><strong>Cannot replace a lawyer:</strong> Your specific case may have nuances requiring professional legal advice</li>
            <li><strong>Cannot guarantee outcomes:</strong> Legal matters depend on many factors including evidence, court discretion</li>
            <li><strong>Cannot represent you:</strong> You still need a lawyer for court appearances</li>
            <li><strong>Cannot handle highly complex cases:</strong> Criminal trials, corporate law, constitutional matters need expert lawyers</li>
          </ul>

          <h3>Disclaimer</h3>
          <blockquote>
            <p><strong>Important Legal Disclaimer:</strong></p>
            <p>NyaySetuAI provides legal information, not legal advice. The information is for educational purposes and should not be considered a substitute for professional legal counsel. For serious legal matters, always consult a qualified lawyer. We do not guarantee the accuracy, completeness, or applicability of the information to your specific situation.</p>
          </blockquote>

          <h3>When to Consult a Lawyer</h3>
          <p>You should definitely consult a lawyer if:</p>
          <ul>
            <li>You're facing criminal charges</li>
            <li>Large sums of money are involved</li>
            <li>Property disputes or inheritance</li>
            <li>Complex contract negotiations</li>
            <li>Court representation is needed</li>
            <li>Case involves multiple parties or jurisdictions</li>
          </ul>

          <h3>AI Accuracy & Confidence</h3>
          <ul>
            <li><strong>High Confidence (85%+):</strong> Well-established legal concepts, common IPC sections</li>
            <li><strong>Medium Confidence (70-85%):</strong> Less common scenarios, interpretation-dependent laws</li>
            <li><strong>Low Confidence (< 70%):</strong> System will recommend consulting a lawyer</li>
          </ul>

          <h3>Feedback & Improvement</h3>
          <ul>
            <li>Report incorrect or unhelpful responses</li>
            <li>Suggest improvements to document templates</li>
            <li>Help us identify biases or errors</li>
            <li>Your feedback makes the system better for everyone</li>
          </ul>

          <h3>Responsible Use</h3>
          <p>Users are expected to:</p>
          <ul>
            <li>Provide honest, accurate information</li>
            <li>Not misuse the platform for illegal purposes</li>
            <li>Understand the limitations of AI-generated content</li>
            <li>Seek professional help for serious matters</li>
          </ul>
        `,
      },
    ],
  },

  // 6. ABOUT THE PROJECT
  {
    id: "about-project",
    title: "About the Project",
    pages: [
      {
        id: "project-overview",
        title: "Project Overview",
        content: `
          <h2>Project Overview</h2>
          
          <h3>Project Title</h3>
          <p><strong>NyaySetuAI: AI-Powered Legal Assistance Platform for Accessible Justice</strong></p>

          <h3>Project Summary</h3>
          <p>NyaySetuAI is an innovative legal technology platform that leverages artificial intelligence, natural language processing, and blockchain technology to democratize access to legal information and services in India. The platform addresses the critical gap between India's complex legal system and ordinary citizens who struggle to understand their rights and navigate legal procedures due to cost, complexity, and accessibility barriers.</p>

          <h3>Key Innovations</h3>
          <ul>
            <li><strong>AI-Powered Legal Assistant:</strong> Uses advanced NLP and legal-domain LLMs to understand citizen queries and provide accurate legal information</li>
            <li><strong>IPC Section Prediction:</strong> Machine learning model trained on legal datasets to automatically identify applicable IPC sections</li>
            <li><strong>Document Automation:</strong> AI-generated legal documents (FIRs, RTI, bail applications, notices) using verified templates</li>
            <li><strong>Blockchain Integration:</strong> Secure, tamper-proof storage and sharing of legal documents</li>
            <li><strong>Voice Interaction:</strong> Speech-to-text and text-to-speech for low-literacy users</li>
            <li><strong>Citizen-Friendly Interface:</strong> Converts complex legal jargon into simple, everyday language</li>
          </ul>

          <h3>Technology Stack</h3>
          
          <h4>Frontend</h4>
          <ul>
            <li><strong>Framework:</strong> Next.js 16 (React)</li>
            <li><strong>Styling:</strong> Tailwind CSS with dark mode support</li>
            <li><strong>UI Components:</strong> Radix UI, Magic UI, Framer Motion</li>
            <li><strong>State Management:</strong> React Hooks</li>
          </ul>

          <h4>Backend</h4>
          <ul>
            <li><strong>API Framework:</strong> FastAPI / Flask (Python)</li>
           <li><strong>Authentication:</strong> Better Auth with OAuth (GitHub, Google)</li>
            <li><strong>Database:</strong> MongoDB (user data, documents metadata)</li>
            <li><strong>Blockchain:</strong> Custom blockchain implementation for document storage</li>
          </ul>

          <h4>AI/ML</h4>
          <ul>
            <li><strong>Large Language Model:</strong> Gemini (Google) for legal query understanding</li>
            <li><strong>Vector Database:</strong> ChromaDB / FAISS for legal knowledge retrieval</li>
            <li><strong>Embeddings:</strong> Sentence transformers for semantic search</li>
            <li><strong>IPC Prediction Model:</strong> Fine-tuned transformer model on legal datasets</li>
          </ul>

          <h4>Deployment</h4>
          <ul>
            <li><strong>Frontend:</strong> Vercel</li>
            <li><strong>Backend:</strong> Render</li>
            <li><strong>Database:</strong> MongoDB Atlas</li>
            <li><strong>Chatbot API:</strong> Render (https://vois-nyaysetu-chatbot.onrender.com)</li>
          </ul>

          <h3>Target Users</h3>
          <ul>
            <li>General citizens facing legal issues</li>
            <li>Students learning about Indian legal system</li>
            <li>Small businesses needing legal documentation</li>
            <li>NGOs working on legal awareness</li>
            <li>Rural communities with limited access to lawyers</li>
          </ul>

          <h3>Social Impact</h3>
          <ul>
            <li><strong>Cost Reduction:</strong> Saves citizens thousands of rupees in legal consultation fees</li>
            <li><strong>Time Efficiency:</strong> Instant help instead of days/weeks of waiting</li>
            <li><strong>Legal Literacy:</strong> Educates millions about their rights and legal procedures</li>
            <li><strong>Access to Justice:</strong> Reaches underserved rural and remote areas</li>
            <li><strong>Empowerment:</strong> Enables citizens to take informed legal actions</li>
          </ul>

          <h3>Future Roadmap</h3>
          <ol>
            <li><strong>Phase 1 (Current):</strong> Core features - chatbot, document generation, blockchain storage</li>
            <li><strong>Phase 2:</strong> Multilingual support (Hindi, Tamil, Telugu, Bengali, Marathi)</li>
            <li><strong>Phase 3:</strong> State-specific laws and procedures</li>
            <li><strong>Phase 4:</strong> Mobile app for Android/iOS</li>
            <li><strong>Phase 5:</strong> Court case tracking and legal updates</li>
            <li><strong>Phase 6:</strong> Integration with government legal aid programs</li>
          </ol>

          <h3>Recognition & Awards</h3>
          <ul>
            <li>Developed for hackathon/academic project</li>
            <li>Showcases intersection of AI, legal tech, and social impact</li>
            <li>Demonstrates practical application of blockchain for public good</li>
          </ul>
        `,
      },
      {
        id: "team-contact",
        title: "Team & Contact",
        content: `
          <h2>Team & Contact Information</h2>
          
          <h3>Project Team</h3>
          <p>NyaySetuAI is developed by a dedicated team of developers, designers, and legal enthusiasts committed to making justice accessible to all.</p>

          <h3>Contact Us</h3>
          <p>For questions, feedback, or collaboration opportunities:</p>
          <ul>
            <li><strong>Website:</strong> <a href="https://nyay-setu-prod.vercel.app" target="_blank">https://nyay-setu-prod.vercel.app</a></li>
            <li><strong>Email:</strong> support@nyaysetuai.in (example)</li>
            <li><strong>GitHub:</strong> Project repository link</li>
          </ul>

          <h3>Contribute</h3>
          <p>We welcome contributions to improve NyaySetuAI:</p>
          <ul>
            <li><strong>Report Bugs:</strong> Found an error? Let us know</li>
            <li><strong>Suggest Features:</strong> Have ideas for new capabilities?</li>
            <li><strong>Legal Expert Review:</strong> Help verify AI responses</li>
            <li><strong>Translation:</strong> Assist with regional language support</li>
            <li><strong>Documentation:</strong> Improve user guides and tutorials</li>
          </ul>

          <h3>Acknowledgments</h3>
          <p>We thank:</p>
          <ul>
            <li>Open-source community for tools and libraries</li>
            <li>Legal experts who provided guidance</li>
            <li>Early testers who provided valuable feedback</li>
            <li>Government of India for accessible legal databases</li>
          </ul>

          <h3>Disclaimer</h3>
          <p>NyaySetuAI is an educational and informational platform. It does not provide legal advice and does not establish an attorney-client relationship. Users should consult qualified lawyers for professional legal counsel.</p>

          <h3>License & Terms</h3>
          <ul>
            <li><strong>Platform Use:</strong> Free for personal, non-commercial use</li>
            <li><strong>Content:</strong> Legal information sourced from public government databases</li>
            <li><strong>Privacy:</strong> See our Privacy Policy</li>
            <li><strong>Terms of Service:</strong> See Terms of Use</li>
          </ul>

          <h3>Support the Project</h3>
          <p>NyaySetuAI is a non-profit initiative. You can support us by:</p>
          <ul>
            <li>Sharing the platform with those who need legal help</li>
            <li>Providing feedback to improve accuracy</li>
            <li>Spreading awareness about legal rights</li>
            <li>Contributing to open-source development</li>
          </ul>

          <h3>Version Information</h3>
          <ul>
            <li><strong>Current Version:</strong> 1.0.0</li>
            <li><strong>Last Updated:</strong> January 2026</li>
            <li><strong>Platform Status:</strong> Operational</li>
          </ul>
        `,
      },
    ],
  },

  // 7. TECHNICAL ARCHITECTURE
  {
    id: "technical-architecture",
    title: "Technical Architecture",
    pages: [
      {
        id: "system-architecture",
        title: "System Architecture",
        content: `
          <h2>System Architecture</h2>
          <p>NyaySetuAI follows a modern, scalable architecture designed for performance, security, and maintainability.</p>

          <h3>Architecture Overview</h3>
          <p>The platform uses a <strong>three-tier architecture</strong>:</p>
          <ul>
            <li><strong>Presentation Layer:</strong> Next.js frontend with responsive UI</li>
            <li><strong>Application Layer:</strong> FastAPI/Flask backend with AI processing</li>
            <li><strong>Data Layer:</strong> MongoDB for data storage + Blockchain for documents</li>
          </ul>

          <h3>Component Breakdown</h3>
          
          <h4>Frontend (Next.js)</h4>
          <ul>
            <li><strong>Pages:</strong> Server-side rendered pages for SEO and performance</li>
            <li><strong>Components:</strong> Reusable UI components (Navbar, Footer, Chatbot)</li>
            <li><strong>API Routes:</strong> Next.js API routes for backend communication</li>
            <li><strong>State Management:</strong> React Context + Hooks for global state</li>
          </ul>

          <h4>Backend Services</h4>
          <ul>
            <li><strong>Authentication Service:</strong> Better Auth with OAuth providers</li>
            <li><strong>AI Service:</strong> Gemini API integration for legal queries</li>
            <li><strong>Document Service:</strong> PDF generation and template processing</li>
            <li><strong>Blockchain Service:</strong> Document storage and verification</li>
          </ul>

          <h4>Database Schema</h4>
          <p><strong>MongoDB Collections:</strong></p>
          <ul>
            <li><strong>users:</strong> User profiles, authentication data</li>
            <li><strong>chats:</strong> Conversation history</li>
            <li><strong>documents:</strong> Document metadata and references</li>
            <li><strong>blockchain_records:</strong> Transaction hashes and timestamps</li>
          </ul>

          <h3>Data Flow</h3>
          <ol>
            <li>User interacts with frontend (Next.js)</li>
            <li>Frontend sends request to API route</li>
            <li>API route authenticates and validates request</li>
            <li>Backend service processes request (AI, database, blockchain)</li>
            <li>Response sent back through API route to frontend</li>
            <li>Frontend updates UI with response</li>
          </ol>

          <h3>Security Layers</h3>
          <ul>
            <li><strong>HTTPS:</strong> All communications encrypted</li>
            <li><strong>JWT Tokens:</strong> Secure authentication</li>
            <li><strong>Input Validation:</strong> Sanitize all user inputs</li>
            <li><strong>Rate Limiting:</strong> Prevent abuse and DDoS</li>
            <li><strong>CORS:</strong> Controlled cross-origin requests</li>
          </ul>
        `,
      },
      {
        id: "ai-ml-pipeline",
        title: "AI/ML Pipeline",
        content: `
          <h2>AI/ML Pipeline</h2>
          <p>Understanding how NyaySetuAI processes legal queries using artificial intelligence.</p>

          <h3>Query Processing Pipeline</h3>
          
          <h4>Step 1: Input Processing</h4>
          <ul>
            <li>User query received (text or voice)</li>
            <li>Voice converted to text using Speech-to-Text API</li>
            <li>Text normalized and cleaned</li>
          </ul>

          <h4>Step 2: Intent Recognition</h4>
          <ul>
            <li>AI identifies query type (question, document request, IPC lookup)</li>
            <li>Extracts key entities (dates, names, locations, IPC sections)</li>
            <li>Determines user intent and context</li>
          </ul>

          <h4>Step 3: Knowledge Retrieval</h4>
          <ul>
            <li>Query converted to embeddings using sentence transformers</li>
            <li>Vector database (ChromaDB) searches for relevant legal knowledge</li>
            <li>Top-k most relevant documents retrieved</li>
          </ul>

          <h4>Step 4: Response Generation</h4>
          <ul>
            <li>Retrieved context + user query sent to Gemini LLM</li>
            <li>AI generates response in simple language</li>
            <li>Response formatted and structured</li>
          </ul>

          <h4>Step 5: Post-Processing</h4>
          <ul>
            <li>Response validated for accuracy</li>
            <li>Legal disclaimers added where needed</li>
            <li>Response sent to user</li>
          </ul>

          <h3>IPC Section Prediction Model</h3>
          <p><strong>Model Architecture:</strong></p>
          <ul>
            <li>Fine-tuned transformer model (BERT/RoBERTa)</li>
            <li>Trained on 10,000+ labeled legal cases</li>
            <li>Multi-label classification (multiple IPC sections per case)</li>
          </ul>

          <p><strong>Training Data:</strong></p>
          <ul>
            <li>Indian legal case descriptions</li>
            <li>IPC section labels</li>
            <li>Augmented with synthetic examples</li>
          </ul>

          <h3>Document Generation</h3>
          <p>AI-powered document creation process:</p>
          <ol>
            <li>User fills form with required details</li>
            <li>Template selected based on document type</li>
            <li>AI fills template with user data</li>
            <li>Legal language and formatting applied</li>
            <li>PDF generated and returned to user</li>
          </ol>
        `,
      },
      {
        id: "blockchain-implementation",
        title: "Blockchain Implementation",
        content: `
          <h2>Blockchain Implementation</h2>
          <p>How NyaySetuAI uses blockchain technology for secure document storage.</p>

          <h3>Why Blockchain?</h3>
          <ul>
            <li><strong>Immutability:</strong> Documents cannot be altered once stored</li>
            <li><strong>Timestamp Proof:</strong> Verifiable proof of document creation time</li>
            <li><strong>Decentralization:</strong> No single point of control</li>
            <li><strong>Transparency:</strong> All transactions are auditable</li>
          </ul>

          <h3>Blockchain Structure</h3>
          <p>Each block contains:</p>
          <ul>
            <li><strong>Block Number:</strong> Sequential identifier</li>
            <li><strong>Timestamp:</strong> When block was created</li>
            <li><strong>Document Hash:</strong> SHA-256 hash of document</li>
            <li><strong>User ID:</strong> Owner of the document</li>
            <li><strong>Previous Hash:</strong> Link to previous block</li>
            <li><strong>Nonce:</strong> Proof-of-work value</li>
          </ul>

          <h3>Document Upload Process</h3>
          <ol>
            <li>User uploads document (PDF, image)</li>
            <li>Document encrypted with user's key</li>
            <li>SHA-256 hash generated</li>
            <li>Hash stored in new blockchain block</li>
            <li>Block mined and added to chain</li>
            <li>Transaction ID returned to user</li>
          </ol>

          <h3>Document Verification</h3>
          <p>To verify a document's authenticity:</p>
          <ol>
            <li>Retrieve document from storage</li>
            <li>Calculate its SHA-256 hash</li>
            <li>Compare with hash stored in blockchain</li>
            <li>If hashes match → document is authentic and unaltered</li>
          </ol>

          <h3>Sharing Mechanism</h3>
          <ul>
            <li>Owner grants access using recipient's User ID</li>
            <li>Access control list updated in blockchain</li>
            <li>Recipient can view but not modify document</li>
            <li>Sharing event recorded with timestamp</li>
          </ul>
        `,
      },
    ],
  },

  // 8. TROUBLESHOOTING & FAQs
  {
    id: "troubleshooting",
    title: "Troubleshooting & FAQs",
    pages: [
      {
        id: "common-issues",
        title: "Common Issues & Solutions",
        content: `
          <h2>Common Issues & Solutions</h2>

          <h3>Login & Authentication Issues</h3>
          
          <h4>Problem: Cannot log in with email</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Check if email is verified (check inbox/spam)</li>
            <li>Ensure password is correct (use "Forgot Password")</li>
            <li>Clear browser cache and cookies</li>
            <li>Try different browser</li>
          </ul>

          <h4>Problem: OAuth login (GitHub/Google) not working</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Ensure pop-ups are not blocked</li>
            <li>Check if third-party cookies are enabled</li>
            <li>Try logging out of GitHub/Google and retry</li>
          </ul>

          <h3>Chatbot Issues</h3>
          
          <h4>Problem: Chatbot not responding</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Check internet connection</li>
            <li>Refresh the page</li>
            <li>Clear browser cache</li>
            <li>Try shorter, simpler questions</li>
          </ul>

          <h4>Problem: Chatbot gives irrelevant answers</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Be more specific in your question</li>
            <li>Provide context (e.g., "In India, what is...")</li>
            <li>Ask follow-up questions to clarify</li>
            <li>Report issue using feedback button</li>
          </ul>

          <h3>Document Generation Issues</h3>
          
          <h4>Problem: PDF not downloading</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Check browser download settings</li>
            <li>Disable pop-up blocker temporarily</li>
            <li>Try right-click → "Save As"</li>
            <li>Use different browser</li>
          </ul>

          <h4>Problem: Generated document has errors</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Review input data for accuracy</li>
            <li>Regenerate document with corrected information</li>
            <li>Manually edit downloaded PDF if minor error</li>
          </ul>

          <h3>Blockchain Upload Issues</h3>
          
          <h4>Problem: Document upload fails</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Check file size (max 10MB)</li>
            <li>Ensure file type is supported (PDF, JPG, PNG)</li>
            <li>Check internet connection stability</li>
            <li>Try compressing large files</li>
          </ul>

          <h4>Problem: Cannot share document</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Verify recipient's User ID is correct</li>
            <li>Ensure you're the document owner</li>
            <li>Check if document upload completed successfully</li>
          </ul>

          <h3>Performance Issues</h3>
          
          <h4>Problem: Website loading slowly</h4>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Check internet speed</li>
            <li>Clear browser cache</li>
            <li>Close unnecessary browser tabs</li>
            <li>Try during off-peak hours</li>
          </ul>
        `,
      },
      {
        id: "faqs",
        title: "Frequently Asked Questions",
        content: `
          <h2>Frequently Asked Questions</h2>

          <h3>General Questions</h3>
          
          <h4>Q: Is NyaySetuAI really free?</h4>
          <p><strong>A:</strong> Yes, 100% free. No hidden charges, no subscription fees, no premium tiers. All features are available to everyone.</p>

          <h4>Q: Do I need to create an account?</h4>
          <p><strong>A:</strong> Basic chatbot queries don't require an account. However, to save documents, access blockchain features, and maintain conversation history, you need to sign up.</p>

          <h4>Q: Is my data safe?</h4>
          <p><strong>A:</strong> Yes. We use encryption, secure authentication, and blockchain technology. We never sell your data to third parties.</p>

          <h3>Legal Questions</h3>
          
          <h4>Q: Can NyaySetuAI replace a lawyer?</h4>
          <p><strong>A:</strong> No. NyaySetuAI provides legal information, not legal advice. For serious matters, always consult a qualified lawyer.</p>

          <h4>Q: Are the IPC section predictions accurate?</h4>
          <p><strong>A:</strong> Our AI achieves 85%+ accuracy on common cases, but predictions should be verified with legal professionals for important matters.</p>

          <h4>Q: Can I use AI-generated documents in court?</h4>
          <p><strong>A:</strong> Yes, but we recommend having a lawyer review them first. The documents follow standard formats but may need customization for your specific case.</p>

          <h3>Technical Questions</h3>
          
          <h4>Q: Which browsers are supported?</h4>
          <p><strong>A:</strong> Chrome, Firefox, Safari, Edge (latest versions). Mobile browsers also supported.</p>

          <h4>Q: Does it work on mobile phones?</h4>
          <p><strong>A:</strong> Yes, the platform is fully responsive and works on smartphones and tablets.</p>

          <h4>Q: Can I use it offline?</h4>
          <p><strong>A:</strong> Currently, internet connection is required. Offline mode is planned for future updates.</p>

          <h3>Feature Questions</h3>
          
          <h4>Q: What languages are supported?</h4>
          <p><strong>A:</strong> Currently English and Hindi. More Indian languages coming soon.</p>

          <h4>Q: How do I delete my account?</h4>
          <p><strong>A:</strong> Go to Profile → Settings → Delete Account. Note: Blockchain documents cannot be deleted due to blockchain's immutable nature.</p>

          <h4>Q: Can I export my data?</h4>
          <p><strong>A:</strong> Yes, you can download all your chat history and documents from your profile.</p>
        `,
      },
    ],
  },
];
