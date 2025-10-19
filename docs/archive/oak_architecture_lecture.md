# OaK Architecture: A Vision of SuperIntelligence from Experience

**Author:** Rich Sutton  
**Event:** Reinforcement Learning Conference 2025  
**Video Source:** https://www.youtube.com/watch?v=gEbbGyNkR2U

---

## Transcription

**[00:05]** I had so much fun talking with so many of you here today. And you know we need a conference on reinforcement learning. It's clear. I wasn't sure but now I think it's clear. This was the right move.

**[00:21]** So I have prepared for you a talk on the OaK architecture. It's a vision of super intelligence from experience. It really is my attempt to address the issues at the center of AI. And I want to start just by recognizing how difficult and important is the task of AI.

**[00:56]** AI is a grand quest. We're trying to understand how people work. We're trying to make people. We're trying to make ourselves powerful. And this is a profound intellectual milestone. It's going to change everything. You know this, but it's good to take a moment and pause and recognize what we're doing is incredibly hard, incredibly important. As an intellectual milestone, I think it'll be comparable to the origin of life on the earth at least when we, when some part of the planet understands how it works and how it thinks and how it can be so transformative to the planet. 

**[01:42]** Okay. But it's also a continuation of things that we've always done and it's just the next big step. So now myself I think this is just going to be good. Lots of people are worried about it. I think it's going to be good. It's an unalloyed good and I think the greatest advances are still ahead of us. It's a marathon.

**[02:10]** I think you know good for this group that the path to full AI, strong AI, runs through reinforcement learning and not I think through things like non-experiential things like large language models. The biggest bottleneck is strangely is we have inadequate learning algorithms. You may think we have our deep learning and that's the one thing we know but I think it's not like that at all. I think our algorithms are very crude. They need to be better and that is what we should be working on.

**[02:47]** And then myself, I've tried to think deeply about this intelligence for half a century. Every day I'm sort of in the trenches designing algorithms, trying to design algorithms, seeking better algorithms for reinforcement learning, for learning from experience. And I follow this Alberta plan for AI research which you may know about. Mike and Patrick and I did it a couple years ago. And today I'm going to talk about the vision of an overall agent architecture, AI agent architecture, called OaK and I think it provides a line of sight towards our grand prize of understanding mind.

## The OaK Name

**[03:25]** Okay. So those are my introductory comments. Now let's talk about OaK. I think it's fun just to start with the name so you which may be a mystery, OaK. It comes from the idea of options and knowledge. 

**[03:37]** Now, as many of you are very familiar with, an option is a pair. Well, actually, you may think it's a triple. I sort of have dropped the initiation set in my for many last couple decades. So for me, it's a pair of a policy, a way of behaving, and a way of deciding to stop behaving. Okay, so just those two, just a pair. 

**[04:01]** And in OaK the agent has lots of options and it's going to learn its knowledge will be about what happens when you follow the option. So in this way the agent is meant to learn a high level transition model of the world that enables planning with larger jumps and hopefully carves the world at its joints. Yeah so that's where the name is from.

## The Holy Grail of AI

**[04:23]** I think it is a grand challenge and a grand quest. And so I show it like this that we are seeking the holy grail. The holy grail of AI. Let me put that up in a way it's easier to read. We want this AI design that is domain general, contains I'm going to say nothing specific to the world. We want a general idea.

**[05:01]** So let me just put down my three main design goals:
1. It should be **domain general**
2. It should be **experiential** - that is the mind should grow from runtime experience not from a special training phase
3. It should be **open-ended** in its sophistication in its abstractions

**[05:16]** So that it can form any concepts in its mind that are needed to deal with whatever world it's connected to, limited only by its computational resources. So those are the three main desiderata and we'll talk about them.

## Design Time vs Runtime

**[05:35]** I guess first I want to establish some words. I want to talk about design time and runtime. Design time and runtime. When you're in the factory being designed then your robot goes out and lives its world, that's its runtime.

**[06:24]** At design time is when you're building in any of your domain knowledge and then at runtime is when you're actually interacting with the world. Learning from experience, making plans that are specific to the part of the world you're in. So like I don't know a large language model, everything is done at design time and when it goes out to be used in the world it doesn't do anything. My emphasis is going to be the other way around. We want I want to do all the important things at runtime online on the job.

**[06:55]** And in a minute I'll be talking about a big world but the idea of a big world, a big complex world, is that you're not going to be able to build things in it. You're not going to have your agent know everything about the world in the factory because the world is huge and you can't know everything. Your robot is small compared to the world. And so if you want to be able to learn arbitrary open-ended abstractions you need the world to find out whether the right abstractions for the part of the world you're running into. So you got to do it at runtime.

## Should Design Reflect the World?

**[07:44]** So let's just ask the question. Should an agent's design reflect the world in which it's expected to be used?

**[08:05]** Good thing about this question is both answers are wrong. I mean both answers are right. So you can, yeah if you want something to perform well and you want to put it out there and have it do something good right away, you know, you want to put design domain knowledge in there. You want it to reflect the world. But if you want a good design, so I'm gonna say no. My quest, my quest is that the design should not depend on the world at all. Okay. It should be domain general.

**[08:41]** Now this is really just you know there are multiple questions and there are multiple uses and like you know I have to respect totally you know someone who wants to do an application, make something that's useful, make something that performs well. Sure that's important but also important is let's understand the mind in a simple way. Let's what we would want is a conceptually simple understanding of what's going on inside a mind. 

**[09:14]** That is in some sense the grand quest of AI is to understand what it means to achieve goals, what it means to understand an arbitrary world. It should be simple and if you, the world, the actual domain that you're going to interact with is arbitrarily complex and so your goal, your job, your agent's job is to go out there and learn all the fiddly wonky little details and high-level structures of the world that it's going to encounter. But you really don't want to understand what it's doing in terms of all those domain specific details. You want a level of understanding that is at a higher level and is based on principles and not the intricate complex details that are in the world.

## The Bitter Lesson

**[10:25]** So of course I have to reference the bitter lesson at this point. And I'll just read this. The actual contents of minds are part of the arbitrary intrinsically complex outside world. They are not what should be built in as their complexity is endless, genuinely endless. Our agent has a big computer and we don't want to understand everything going on in there. Instead, we should build in only the meta methods that can find and capture this arbitrary complexity.

**[10:59]** In short, we want agents that can discover like we can, not which contain what we have already discovered. So that's the idea for the purpose here in a scientific conference trying to understand what a mind is, how it should work. We want a level of description that is above all those domain specific endless details.

## Learning from Experience Only

**[11:25]** Okay. Now second question: should the agent learn from special training data or should it learn only from runtime experience? Only from runtime experience.

**[11:52]** Well, for me the agent should learn only from runtime experience, should be entirely experiential. And the reason is again we want a conceptually simple design and if it's possible to learn only at runtime that would be a simpler understanding and so we should seek this.

**[12:18]** So the form of the argument is going to be there's certain things that have to be done at runtime and could be done at design time and so basically everything has to be done at runtime, maybe also at design time but at runtime you have to be able to learn, you have to be able to change your abstractions, you have to be able to make a model of the world, you have to be able to plan with that model. All those things have to be done at runtime because you're going to encounter the world. The world might not be like what you expected and certainly you won't know all the intricate details and all the abstractions that are needed for the part of the world that you're interacting with.

**[13:02]** So all those things have to be done at runtime. Now you could also do some of them at design time but it's sort of in some sense that would be optional. You know, that might speed you up, but since they all have to, you have to be capable of being done at runtime, why not make a conceptually simple design and just doesn't worry about trying to get a head start on the problem, but just has the runtime aspects. And so that's what that's the quest I'm setting out on. And I'm hoping you're going to join me.

## The Big World Perspective

**[13:40]** Okay. So I've talked about the big world perspective. So let's make, let's gain a common knowledge amongst us of what that means. The big world perspective or the big world hypothesis, something that's been floating around at least in Alberta for like five years and we've all come comfortable with it. And it really influences all of our thoughts and our designs.

**[14:00]** So the idea is simply that the world is bigger, more complex than the agent. And it's much bigger really. It's bigger than this. It's big, you know, it's really big. And it's got to be much much bigger than the agent because the world contains, you know, billions of other agents and of course all the atoms and all the intricacies of the objects spread around. The world is much more big and the world contains what is happening in all those other agents matters to you. It matters to you what's going on in the minds of your friends and your loved ones and your enemies. All those things are important to you and they have to be taken into consideration.

**[14:52]** And so you know the upshot is that nothing the agent is going to be doing is going to be exact and it's not going to be optimal. It's going to be approximate when you make a value function. It's going to of course be an approximate value function. And your policy will not be the optimal policy. Your transition models will be enormous reductions. They're sitting inside your head. You know, your model of the world and the world is out there much much bigger, right?

**[15:21]** Even a single state of the world, you can never hold it in your head. You can never hold in your head all the states in everyone else's minds. So, one of the most important consequences of this is that the world ends up appearing non-stationary.

**[15:41]** And I'm citing a little paper on this that Dave Silver and a couple and I wrote where we just made this point. The world, if you don't have a model, you don't have a good sense of the state of the world and it's big and sometimes you're there, sometimes you're there, things look the same, your function approximator cannot capture everything, the world's going to look non-stationary and so you have to learn at runtime.

**[16:14]** You can't have built in everything about the whole big world at design time. You have to learn at runtime. You're going to encounter some particular part of the world at runtime and you want to customize and be appropriate for that part. You know, you go to work, you're an AI agent that's supposed to play a productive role in society and it goes to work and it meets its co-workers. It has to remember the name of the guy it's working with. You know, that was not in the domain knowledge. It has to remember the work that they've done on that project. What's working well? What's not working well? What are they trying to do? All those, you know, everything you do in your life is could not have been foreseen.

**[17:04]** So I know it should be obvious you have to learn during your life. You have to plan during your life. Leslie Kaelbling made this point that planning is required because the world is big.

**[17:17]** And so this also applies to your abstractions. You know, my third desiderata is that we want an open-ended abstraction. We want to get more and more sophisticated understanding of this particular world. We have to find, you know, what's the right joints and ideas that are involved in the world that we're encountering. And so, yeah, you may be able to also add abstractions. Maybe you believe in objects like Leslie and you want to build that in, but that doesn't get you out of having to have the ability to create new abstractions at runtime.

**[17:58]** And so, if you're going to have to create them at runtime, you know, why don't we just do it in one place and that'll be a very good start. You know, I think of a design for an AI, the perfect design. It would not be a huge thing. It would not be like an encyclopedia or a library worth of knowledge. It would be like, well, when I make, for me actually it almost fits on a slide. You write in the pseudo code, you know, maybe it's three slides. Okay. I think something of that order. Five pages for your description of all the essential elements that are domain independent and yet are capable of arbitrary open-ended abstractions.

## Why Runtime Learning Wins

**[19:00]** Okay. So this talk like, hey, I was up till like four o'clock last night making these slides. This is sort of a new talk for me. This is the first time you're the first guys hearing it. I've been traveling around the world and giving all these philosophical talks and political talks and point of view talks and that's great and I've enjoyed that but you know I really thought here I'm at the RLC conference, reinforcement learning, I should do something substantive, maybe even technical.

**[19:40]** And then all during the week you know I went to every, I went to all these talks, I talked to all these people. And I keep just changing my mind about what I want to say. And so anyway, this is all my way of excusing myself or explaining to you that this talk is new and it's not quite polished. In particular, I might say some things more than once. And maybe it's okay to have some repetition if they're important things. Okay, but just be aware of that.

**[20:18]** Runtime learning I think always wins over design time because the world is much bigger than the agent, the big world perspective. Design time can't cover every case. Runtime learning can customize to the part of the world actually encountered. Runtime learning scales with available compute whereas design time learning or anything done at design time scales with the available human expertise at design time. It was the only thing available and historically scaling with compute wins in the long run. That's what the bitter lesson is explicitly about.

**[21:01]** However, today's deep learning methods, runtime deep learning methods, continual learning, they don't work very well. Okay, this is a big bitter thing for me. I wish they worked well because I'm talking all about runtime learning and I want to use it.

**[21:23]** Yeah, if we, one last thing about runtime learning, it does enable metalearning. Metalearning is where you like try learning one way and then you try learning another way and you notice that oh this way works better, in the future I will do this. If you were doing everything in one shot you couldn't do that. This idea of becoming better at learning requires one time you're doing learning, another time you're trying a different way of learning and you pick the better one. So metalearning really requires this to be done at the runtime.

## The AI Problem

**[21:59]** Okay. Now let's think about the problem just a little bit more. You know I like to separate things into the problem and the solution. Really almost everything I've been talking to you about is the problem, the quest. What are our goals? What are our desiderata?

**[22:13]** So one more slide on that. The AI problem is to design an effective purposeful agent that acts in the world. And the classic reinforcement problem is the same thing except we add the purpose is specified by scalar reward signal. The reward and the world is general and incompletely known. But the world can be anything, could be grid world or the human world, can be stochastic, complex, nonlinear, non-Markov. The state space of the big world is effectively infinite and its dynamics are effectively non-stationary.

## The Reward Hypothesis

**[22:58]** Let me go ahead to just talk about this one a little bit further. The purpose is specified by a scalar signal. So that's, we have a name for this idea. It's called the reward hypothesis. And I wanted to bring this up because we have thought about it and it's not like a quick choice without intention.

**[23:17]** So the reward hypothesis is this: that all of what we mean by goals and purposes can be well thought of as the maximization of the expected value of the cumulative sum of a received scalar signal called reward.

**[23:35]** So there's lots of specific things there like the expectation, like the cumulative sum. Yeah, and that's been thought through. And the idea of a scalar reward, I just want to say it's not just something we haven't thought about. In fact, it's a great thing. It's a really clear way to specify the goal. It's become popular in many different disciplines, not just AI, but also economics and psychology, control theory, and forever people have been trying to modify. They've been trying to add things like constraints, multiple objectives, risk sensitivity, and I don't know. I hate that. I mean, even if it was good to do, I don't want it to be done. I don't want it to be true.

**[24:32]** I think you've already gotten the sense. I like things to be simple. You know, that's like a really high desiderata, desire. I want things to be simple and I might even simplify them a little bit too far in order to be clear and so anyway, I want things to be simple. Do we need all these things to get generality? That's the real question.

**[24:54]** And Michael Bowling and others have written this really nice paper called "Settling the Reward Hypothesis" where they go through all these cases and they establish that in a certain sense the reward hypothesis is correct that you don't add generality by adding multiple objectives or risk sensitivity or any of these constraints. So it's one way of validating that choice and you might also probably know the "Reward is Enough" paper where we argue that even a simple reward can lead to all the attributes of intelligence in a sufficiently complex world.

## Solution Methods and Architectures

**[25:41]** Okay. So now I want to talk about the solution methods, the architectures. Obvious starting place is model-free reinforcement learning, basic reinforcement learning where the agent constructs a policy and value function at runtime. Both these are functions, all these are runtime RL architectures. The model-free and then you can handle the non-Markov case if you construct your feature state representation from your data.

**[26:18]** But still better would be to make a model of the world and use that model to plan with, potentially better. Now the OaK architecture is along the same line of improvement, of extension and the thing about the OaK architecture is it adds to those things auxiliary problems, subproblems and those sub problems are in the form of attaining individual features, individual state features and in this way we enable the discovery of higher and higher levels of abstraction and we achieve this open-ended goal.

## The OaK Architecture Diagram

**[27:00]** Okay. So, as a picture, this picture on the left is from the textbook, the reinforcement learning textbook. And this is the very last figure in the book. And so maybe it's familiar to some of you. We have the world and then the agent is everything above the world. It's the policy and value functions. It's a model of the world. It's a planner. And it's the U-box. The U-box. I want you to notice because this is a kind of reinforcement learning where we don't assume that the state is available to the agent. Only observations are available to the agent. We send actions to the world. The world sends back observations and a reward.

**[27:46]** Okay. And then there's a process here that's a part of the agent that computes something that we'll use as a state representation by the policy and value function. Okay. So that's the construction process and nowadays I draw things a bit differently.

**[28:09]** And the right figure is the full OaK architecture and you see many of the same components. This U-box is now called perception. Perception is a better name for it because what does it do? This perception process, it takes in the data that's happening, the actions and the observations and it forms a sense of where the agent is now. That's really what perception is about. Take in your sensory input, get a sense of where you are now. Use that sense to make your decisions, as input to your policies, your value functions and your models.

**[28:45]** Okay, so the OaK architecture has all those things, but it also adds auxiliary subproblems and each subproblem will have its own value function and its own policy. So that's what's suggested by having these shadow policies behind the main policy and these secondary auxiliary value functions behind the main value function.

**[29:13]** Also each one of these subproblems is going to be based on a different component of the state feature representation. So this is the thing that acts like state and I want you to think of it as a feature vector and each one of these sub problems is going to be based on a different component of that feature vector. So that's what it looks like as a picture.

## The Eight Steps of OaK

**[29:39]** Okay. Now we're going to get into a bit of the nitty-gritty. We're going to look at it. I've given all these quick introductions to the idea, told you various properties of the OaK architecture. Now I want to tell you exactly what it is or it is these eight steps done in parallel at runtime.

**[29:58]** Okay, it's a lot of steps. I'm going to come back to this slide a bunch of times and develop each part of it. So just relax and let's get started. Let's just learn what some of the characters are here and how they interrelate.

**[30:13]** So we might start with the first line. And this line is learning the policy and the value function for maximizing rewards. That's like normal reinforcement learning. And I think that is almost done. If it was done, there would be a green check mark, but it's blue. And blue means it would be done if we could do this continual deep reinforcement, deep learning thing with metalearning. You know if we really could do continual learning that would be that would be done. And so we can do this in very simple simplified cases. We can deal with some of the algorithms like continual backprop. We can deal with the linear case. So this gets a blue check mark, conceptually done but really it's waiting to be done well. It's waiting to solve this problem of continual learning for deep learning.

**[31:16]** Now the next one is red because we don't really have a solution. We have lots of ideas but we don't have a specific proposal and so I'm going to come back to this later. The second one is generating new state features from the existing features. 

**[31:33]** And let me go over this next bit quicker. Let me just run all the way down verbally through all eight steps. We're going to have some features. We're going to order the features. We're going to take the highest ranked features, the most important features according to our estimation, and we're going to create subproblems of achieving them. 

**[31:55]** So if I decide that being in this lecture room is an important sub goal, I would make a sub problem for that that would succeed when I am here. If I think holding this microphone up sufficiently close to my mouth is a good sub goal. I would make that feature into a good subproblem and so on for finding the restroom and finding the coffee. Coffee is a really good feature for that flowing into your mouth and getting all the sensations involved in that. So that feature becomes a subproblem for attaining it and then you learn solutions.

**[32:43]** So this is the heart of the OaK architecture is to have sub problems. You learn the solutions of the sub problems. The sub problems are the options from the O in OaK. And we also have to learn the value functions that are associated with the sub problem. Okay. And then we're going to have these options.

**[33:02]** And the next step is we're going to learn models of the option. We want to know what will happen if you were to execute any one of them. This will be part of your model of the world but it will be a high level model of the world because it'll be about an extended way of behaving rather than about a single action. These models will enable you to plan and then you so those are all the full main steps.

**[33:33]** Okay. So you've seen it once. You're going to have to maintain metadata on the utility of everything and curate, throw some things out and propose new ones. Okay. So now we're going to go through these steps and for a while I'm going to spend a lot of time actually on the fourth one but yeah the ordering the features it seems kind of easy but we can't do it until we have all the rest, all the other pieces done.

## Creating Subproblems from Features

**[34:03]** Okay let's spend some time about the creation of the subproblems, one for each highly ranked feature. Okay. So acknowledge there's a long history of looking at subproblems that are distinct from the main problem. People talk about curiosity, intrinsic motivation, auxiliary tasks. Some things are settled, some things are unsettled.

**[34:28]** You don't have to read all this. I want to direct your question to the red part. The key open questions about subproblems: which are what should the subproblems be? Where do they come from? How can the agent or can the agent generate its own subproblems and how do the sub problems help on the main problem? 

**[34:49]** So the contribution of OaK is to propose answers to all these questions and to really answer questions like the third one, how can the agent make its own subproblems in the affirmative and thus get open-ended abstraction.

**[35:06]** I like to think of it very basically that we have problems and solutions and these interact with each other. We propose a problem to work on. We work on it. We solve it. As a part of solving it we will make new features and those features will then be the basis for new sub problems and then the sub problems will have to be solved, new features and so on in an endless cycle. Roughly. That's what I'm talking about.

## Examples from Nature

**[35:35]** And I wanted to give some examples from nature. Here's an orangutan, a young orangutan playing, swinging. And so what is he doing? Like he's not getting food. He's just interested in what it feels like when he swings. Yeah. Okay. That's what I think he's doing. I think that sensation is interesting. and he got it once and now he's trying to get it again and understand how to control it.

**[36:09]** Yeah, so here's and also on the other slide we have an orca who somebody threw this big, I don't know what to call it right now, a buoy into his pen and he's decided trying to figure out what he could do with it. And he's managed to get it up on his back. So, that was not random. He got this idea and now he's perfecting it.

**[36:41]** Yeah. So, animals play, people play, infants play, young people play. So, this is a sped up video of an infant playing. And this is what we want. We want the way the child goes from object to object, learns a little bit about it, gets bored, moves on to the next object, and just gradually develops a better and better understanding. Maybe next time when he comes back to the object, he'll have an increased ability, be able to do new things with it.

**[37:21]** This is what we want. And so I'm trying to think about them as posing sub problems for themselves, things to learn about, things to understand, things to predict, and things to control and figure out where it can make progress in learning solving the sub problems.

## Creating Subproblems in a Domain Independent Way

**[37:39]** Okay, so maybe you're ready to accept this statement. The agent must create its own sub problems. Sub problems can't be given to you. Can't be given to you at design time. You've got to create your own that's far too various and world dependent to have been built in. We have to give the responsibility of the questions, the problems, not the solutions, not the features, the questions.

**[38:08]** Okay what is the, how can we do this? I mean we have much of the machinery, the machine of options, general value functions, off policy learning, planning methods. These are machinery to help us in this process but we want to create them in a domain independent way and that's challenging.

**[38:28]** Okay. So I want to offer this possible way to make subproblems in a totally domain independent way which is when you come across a feature, when you make up a new feature or you experience a new feature, you can make it to be the basis of a sub problem. I call it a reward respecting subproblem of feature attainment. So let me show you exactly what that is.

**[38:52]** How do we create a subproblem from a feature? So a feature is like, yeah, feature i. It's a bright light that you saw once. It's an interesting sound that happened. It's you're a baby and you heard the rattle make a sound. You'd like to reproduce that sound. So you have a feature i, a feature index i, and you have kappa which is how intensely you want that feature. You have to express that and you'll get different subproblems if you want it at all costs or if you just kind of want it a little bit.

**[39:27]** So the sub problem is to drive the world to a state where the feature is high without losing too much reward because you will lose some reward if you're not doing what you normally do because what you normally do is maximize reward. There is just one reward by the way and so I don't have to qualify that is the real reward and the sub problem is to achieve a state where the feature is high without losing too much reward without having to go through something that's painful or having lost opportunities to get something pleasurable.

**[40:04]** Okay, so we're trying to find an option. An option is a pair. It's a policy π, termination function γ that maximizes the value of the i feature at termination while respecting the rewards and values. 

**[40:16]** So here's the equation. Maybe we can understand the equation. In each state you're trying to choose, you're going to choose π and γ to maximize. And it's the sum, the sum is conditional on starting the world in the indicated state because yeah for each state we say if we started there, have a policy π that gets you rewards from t+1 to T. T is the time of termination. You're going to follow the option π and you're going to terminate when γ says terminate. And so that will fix, establish the random variable which is the time which you terminate, capital T. And if you look at all the rewards you receive while you are following the option summing them up. Those are the things that you want to be as big as possible or at least negative as possible.

**[41:21]** And then you want to reward yourself for achieving feature i at time of termination, S sub capital T. And you know there's a weighting by kappa. So you want lots of rewards. You want the feature to be true but you know it's got to be traded off the rewards. 

**[41:43]** And you also care about the state that you're in at the time of termination. You don't want to like find a really good way to I don't know get some coffee but has the consequence that you have to break your leg. Okay. Actually, that would be a reward. That would be a bad reward. You don't want a way to get coffee that would leave you in a bad state. Like let's say you got coffee but you know you're gonna get arrested or you're going to fall down the stairs. Okay. Those are bad states.

**[42:28]** You know I often you know walk along the edge of a cliff but don't fall off. If you fall off, it actually doesn't hurt very much to fall off because, you know, if you can say just terminate while you're in the air, the rewards are fine, but the value, the value is, you know, bad rewards are coming up. So, your value will be poor.

**[42:47]** Okay, that's how we create a sub problem. And now let's really we're getting into the heart. We have these processes. The first one is we form the problem just as we just talked about, you know, given a feature form a problem. We do that with all the highly ranked features. So now we have you know dozens of problems. Each one we work on it to produce an option. The solution to sub problem is an option.

**[43:14]** Now you've got these options. Well that defines a correct transition model for the option. Is it well defined? What we know what the model should be. If you give me the way of behaving and the way of terminating, we know what the model should be. And so this is something you work on. You work on computing this model, approximating that model. 

**[43:42]** Once you have the model and you have models of all the different options for all the different subproblems for all the different features and once you have the model, you use the model of course to plan and to improve your behavior. Okay. So we got these three steps and there's one fourth step which is that you have to come up with features right we started with the highly ranked features so we have to have a way of ranking the features.

**[44:10]** And I just want to point out that we have that because all of these three pillars, the later three, all use features to do their job right. If you're going to find the option, the option is a function of state and so you have to look at state features. When should you do the option? When is the value function of the option, when should it have which values? It's going to look at the state features to make those decisions. When you learn the models of the options you're going to look at the state you start in and you're going to look at the state features of that state and you're going to say oh that feature I found useful, that other feature was useless to me.

**[44:48]** And then when you use the models you will find some models are useful. And that will sort of trickle back to evaluate the choice of the options. And that will also trickle back to evaluate the choice of the feature attainment problems. And at least all these learning processes, predictive learning processes will use the features and they will provide feedback to the features saying these are the ones that have proven useful to us. These ones have not.

## The Cycle of Problem Posing and Solving

**[45:21]** Okay. So let's draw the same idea with a different picture. I'm going to have many pictures about the same idea and I'm going to say it a few times so maybe you'll get it. So the perception process is responsible for constructing interesting state features. The play process or the problem posing process, problem posing and solving. That's where you do the sort of core reinforcement learning things of figuring out your value functions and your policies and you produce the options.

**[45:52]** And then you have to predict the consequences of those options to form a transition model. And then of course you plan with the transition model to get improved policies and values. And the feed, we close the cycle is we have feedback from the later steps back to the construction of features. And that feedback is mainly saying I have found that feature useful or I have not found that feature useful.

**[46:22]** Okay. So here's we're back to our eight steps. We now understand what it means to create the subproblems one for each feature and we also know what it means we've talked about how you learn the solutions and the transition models. Maybe there's I'll say one more slide about that about this topic, how we learn those things.

**[46:43]** Oh, but also notice they're in blue because although we know how to do these things, we don't really know how to do them with continual deep learning or maybe we have to use Shaban's continual backprop. You know this is a topic we'll come back to. This is incompletely understood. So we kind of know how to do them but we definitely think we can do better.

## Standard Off-the-Shelf Algorithms

**[47:05]** Okay, one short slide more about that is it to a large extent we could use just standard off-the-shelf algorithms, standard usually off policy algorithms for learning general value functions like GTD and emphatic TD and retrace and ABQ. These are prediction learning methods for generic GVFs and so we can use that to learn the main problem how to get reward. We can learn that for learning diagrams for the sub problems. We can find the transition models of the options with these methods and the planning can also be done with standard algorithms applicable to all GVFs.

**[47:49]** And this enables us to say that anything that can be learned can also be planned. That's I just wanted to get to that slogan for you because it's a good one. It's a bit advanced but it's almost a next step.

## Planning with Options

**[48:06]** Okay, so we got those things and now the other big step and I'm going to have to do it a little bit not in full detail, but we have to talk about how the planning works. Okay, how does the planning going to work? And I'm going to give that a green check mark because I think we do understand this.

**[48:20]** So planning, why do we plan? Why do we want these jumpy temporally extended models of the world, the option models? And but basically why do we want to plan at all? We want to plan because the world changed and the correct values change and it's easier in many cases not in every case but in many cases it's easier to get the model of the world right than to get the values right. So you get the model right and then you do the planning to make the values consistent with your model.

**[48:52]** And so in this big world setting it's the world changes or appears to change. Most of the world's dynamics or in many cases the world's dynamics including the reward parts don't really change but the values nevertheless change. Like it's always true that I can walk over there and find the restroom but it's not always true that I want to go to the restroom. It's not always true that I want to get coffee. It's not always true that I want to go to the library all the things or go to Edmonton. So to prepare for these later wants, these different values, you plan and this also has some implications for which sub problem is useful.

**[49:33]** Okay. Now how does planning work? I like to think that planning is by approximations to value iteration. So this equation is value iteration. You may already know it, but I think maybe you should look first here. What is the model? Model is something that takes a state, a low-level model takes a state and an action, gives you a probability distribution over next states and the expected reward along the way.

**[50:06]** And so value iteration then says I'm trying to improve the values of some states. I look at the possible actions and I'm going to maximize over them. I'm going to look at the immediate reward and I'm going to discount and then take the probability or really the expected value of the value of the next state. So this is the probability of each next state. You weight by that, you take the value of the next state. So you know you probably are familiar, value iteration works like that.

**[50:35]** And really all planning methods in some sense work like this just applied to different states in the search tree and you know order which states are updated in such a way is varied. Okay.

**[50:57]** And the interesting thing about planning with option models is that it's the same. It's really the same. Although life is lived one step at a time, we have to plan it at a higher level. So our knowledge of the world should be about the large scale dynamics. It should not be conditional on single actions but on a sustained way of acting that is on an option.

**[51:18]** So if we look at the conventional model, it receives an action. An option model you receive an option, still you get a probability distribution perhaps over the next states and expected reward, not a one-step reward but some reward while you're following the option and then value iteration is almost unchanged. We just change the actions into options and we still talk about the reward for following that option and the probability of each next state under the option. Okay, so that's good. 

**[51:56]** That gives you a flavor of how planning would be done. You basically you say oh here's some state. What are the things I could do there? What's the best I could do? I'll update my value and here's I could imagine another state. Maybe it's the state I'm in. Maybe it's not the state I'm in. But I go through this outer loop of considering various states and then maxing over the possibilities and doing this equation.

**[52:22]** But I'm sure you are concerned because I've been talking about V of S which is the value of an individual state and we can't do that of course we have to have function approximation. So I don't know I don't think it's that helpful to go through these equations but yeah the value V of S will become the approximate value of a state given a parameter vector W and also your model of the world will become R hat and P hat, they also become parametric and then after you've done that things are much the same.

**[53:00]** There are more complications which I will skip having to do with what's computationally expensive. You can ask me about that if you want. If you're interested, I'll say some summary things.

## Continual Deep Learning Challenge

**[53:19]** So, so we're maybe we're almost done, but remember I said we would come back to some things. So, I said we would come back to the first two, learning how we're going to learn these things and what the problems we have. I want to say explicitly what the situation is there. So two more slides.

**[53:43]** So the OaK architecture requires reliable continual learning, continual deep learning. And so this is one of those things that I said this would be we'd be all done with step one if we could do continual learning. And but we can't, can we do this yet? Okay. Can we do this? Okay. Do we have reliable continual learning?

**[54:02]** Well, we do have reliable continual learning for the linear case, for the tabular case, but for the nonlinear case, for the deep learning case, we can't, we don't yet. Do we? No, we sort of do. We have we have these catastrophic failures like catastrophic forgetting and the catastrophic loss of plasticity that have been figured out long ago and also very recently.

**[54:40]** So we have these catastrophic problems but we also, it looks like there's a range of solution methods. So I guess this is an area that's that's right now in flux and people are figuring things out and you know we're not there I can't give it a green check okay but but there are lots of ideas. Continual backprop is one of them, the metalearning of new features I think can also help.

## Generating New State Features

**[55:03]** And related to that it's the other step that I wanted to talk about where we having to do with creating, generating new state features. This is also a super old problem going back to the 1960s like Minsky and Selfridge would talk about this. They would talk about representation learning. They would talk about the new terms problem and anyway I like to talk about metalearning nowadays.

**[55:28]** So backprop back in '86 was supposed to solve this. We were supposed to you know learning representations by gradient descent. But it really just doesn't. And I think we accept, we recognize that unless we are still in love and think that gradient descent is enough for everything.

**[55:53]** Most of the other methods other than gradient descent are based on generate and test ideas where you like generate a bunch of features and then you test them to see if they're useful and so you could generate them randomly and you could test by their utility and continual backprop is an instance of that. It also has a real old history. Leslie Kaelbling did some of this work in her PhD thesis in 1993. Rupam Mahmood and I did some work a decade ago.

**[56:22]** There's lots of ideas but not yet a specific proposal for a whole network based on grad descent or any other. There aren't, I anyway don't have a specific proposal to solve this problem. I think it's a really really important problem and I think it's like maybe it will be worked out in the next couple of years and then it will literally take over everything that people have done with deep learning. If we had a deep learning method that can do everything we're doing now but can also learn continually that would just be a really big thing and I think there's no reason why it couldn't happen. And so I think it will.

**[57:08]** I also think that something like my algorithm called IDBD and it's really old will be a key part of that solving this problem.

## Summary: The Virtuous Cycle

**[57:28]** Okay. I'm sort of done. This figure was just to remind you one more time of the cyclical nature, how we have state features that produce sub problems that are solved, produce options that are used to form models and this doesn't look like a cycle but remembering that there's feedback being sent from each user of the features, information on which features are useful, which ones aren't. That informs the features and so it is in fact a cycle.

## What Has OaK Achieved?

**[58:04]** So in my quest have we succeeded? We have something that's totally domain general, there's nothing in it specific to any world. It's totally experiential and has the claim or the hope that it will be able to find unlimited open-ended abstractions limited only by the computational resources and so we might ask you know what should one think about this?

**[58:31]** And so I think arguably reinforcement learning and OaK offer the first plausible mechanistic answer to several important questions:
- How can high level knowledge be learned from low-level experience? 
- Where do concepts come from? 
- How do we reason? What is reason? Perhaps reason is just planning in this way
- What is the purpose of play? To find these subproblems which structure our cognition
- What is the purpose of perception? We're answering the question of how perception can operate without reference to a human label or to an external world. Perception can be concepts that have been formed to solve problems that are the basis of subproblems

**[59:26]** And if you know about cognitive science, David Marr, then we would say that OaK is a computational theory of intelligence.

## For the RL/AI Scientist

**[59:33]** Okay. Now, what about someone like yourself, a reinforcement learning AI scientist? I would hope that you would think that OaK provides a way to think about the parts of AI and their interaction and this can guide future research. 

It's a vision for how to do:
- Planning with a learned model which is a key missing ability for today's AIs
- A view of perception that's grounded in experience rather than in human labels
- Incomplete, admittedly incomplete but schematic answers to the discovery problem: Where do the subproblems, options and features come from?

**[1:00:07]** So it's a vision of how we can obtain an open-ended super intelligence entirely grown from experience, even if it's not yet fully specified and even if there are things that I'm saying we don't really know how to do but we should know how to do such as solve continual learning and metalearning.

**[1:00:31]** It's a vision of how to grow a super intelligence from experience at runtime in its most important capabilities and does it: act, learn, plan, model learning, sub problems, the options with all the rest and the discovery of the state features and thereby of the problems, options and models leading into this virtuous open-ended cycle of discovery and is completely general and is thus scalable and a potentially lasting impact.

**[1:00:58]** Thank you very much.

---

*[Applause]*