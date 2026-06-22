# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My inital UML design will present the owner + pet info where the user inputs their name, pet's name, pet's age, and pet's breed. One method would be adding another pet if owner owns more than 1 pet. Then it has to-dos tasks where user inputs the pet care tasks, setup priorities, setting up time, and their availability. Lastly is including owner's day plan where after user creates a task it will generate a schedule. It will display top priorities, total duration, and the date. 

- What classes did you include, and what responsibilities did you assign to each?
I created 4 classes which is Owner, Pet info, To-dos, and Day plan. Owner class responsibilites is inputting owner's name and their availability. One method is addPet(). Pet info class responsibility is inputting pet's name, pet's age, and pet's breed. One method is getPetInfo(). To-dos class responsibility is inputting pet care tasks, priority, time, and availability. One method is setPriority(). Day plan class responsibility is date, taskList, and total duration. The two methods are displaySchedule() and sortByPriority(). 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
