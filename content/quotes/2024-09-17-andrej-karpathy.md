---
title: "Andrej Karpathy on No Priors 80"
date: 2024-09-17
tags:
  - quote
ref: https://www.youtube.com/watch?v=hM_h0UA7upI
---


Quoting Andrej Karpathy from [No Priors #80](https://www.youtube.com/watch?v=hM_h0UA7upI). 

#### Self-Driving Cars

On Tesla vs Waymo:
> I think that Tesla has a software problem and I think Waymo has a hardware problem is the way I put it. I think software problems are much easier. Tesla has deployment of all these cars on earth at scale and I think Waymo needs to get there.

Karpathy is bullish on Tesla winning the TAM of self driving. They do use sophisticated sensors too, but at training time. He thinks the cost savings of large scale vision only hardware will win:
> Tesla actually does use a lot of expensive sensors, they just do it at training time. There are a bunch of cars that drive around with LiDARs, they do a bunch of stuff that doesn't scale and they have extra sensors. They do mapping and all the stuff you're doing at training time, and then you're distilling that into a test time package that has deployed to the cars and is vision only. It's like an arbitrage on sensors.

Tesla self driving will eventually be an end to end neural net outputting driving commands but the volume of training data is too low to do that from scratch so they're building toward it iteratively:
> I think Tesla is kind of eating through the stack my understanding is that current Waymos are actually like not that but that they've tried but they ended up like not doing that is my current understanding but I'm not sure because they don't talk about it but I do fundamentally believe in this approach. And so I think Tesla is kind of eating through the stack. First it just does like a detection on the Image level then it does multiple images gives you prediction then multiple images over time give you a prediction and you're discarding C++ code and eventually you're just giving steering commands and so I think Tesla is kind of eating through the stack.

#### Robotics

Tesla is a robotics company:
> Tesla, I don't think it's a car company. I think this is misleading. This is a robotics company, robotics at scale company. Because I would say at scale is also like a whole separate variable. They're not building a single thing, they're building the machine that builds the thing, which is a whole separate thing.

Tesla found a lot of stuff transferred from cars to Optimus:
> So much transfers. The speed with which Optimus was started, I think to me was very impressive. Because the moment Elon said we're doing this, people just showed up with all the right tools and all the stuff just showed up so quickly, and all these CAD models and all the supply chain stuff.

The roadmap to consumer household robots:
> I think the best customer is yourself first, and I think probably Tesla's going to do this. I'm very bullish on Tesla, if people can tell. The first customer is yourself and you incubate it in the factory and so on, doing maybe a lot of material handling. This way you don't have to create contracts working with third parties, it's all really heavy, there's lawyers involved. You incubate it, then you go, I think, B2B second. And you go to other companies that have massive warehouses. We can do material handling, we're going to do all this stuff, contracts get drafted up, fences get put around, all this kind of stuff. And then once you incubate in companies, I think that's when you start to go into the B2C applications.

#### Transformers

Bullish on the Transformer. Scaling bottleneck is not architecture but data:
> I don't think that the neural network architecture is holding us back fundamentally anymore. It's not the bottom leg, whereas I think before the Transformer it was a bottom leg, but now it's not the bottom leg. So now we're talking a lot more about what is the loss function, what is the data set. We're talking a lot more about those and those have become the bottlenecks almost.

Synthetic data is the only way to keep scaling:
> I think it's the only way we can make progress. We have to make it work. I think with synthetic data you just have to be careful.

Training on "reasoning trajectories" is the path to AGI:
> The internet data is not the data you want for your Transformer. It's like a nearest neighbor that actually gets you really far surprisingly, but the internet data is a bunch of internet web pages. What you want is the inner thought monologue of your brain. That's the trajectories in your brain as you're doing problem solving. If we had a billion of that, AGI is here roughly speaking.

### Humanoid Robots

Why the humanoid form factor for robotics:
> I think people are maybe under appreciating the complexity of any fixed cost that goes into any single platform. I think there's a large cost you're paying for any single platform and so I think it makes a lot of sense to centralize that and have a single platform that can do all the things.

This generalisable platform means the neural network can transfer learn across tasks.

#### Augmenting the Human Brain

Transformers are more efficient than the human brain:
> I think Transformers are actually better than the human brain in a bunch of ways. I think they're actually a lot more efficient system and the reason they don't work as good as the human brain is mostly data issue. Roughly speaking, that's the first story approximation I would say.

> Transformers have a lot bigger working memory and will this will continue to be the case. They're much more efficient learners.

AI as the next layer of the brain, the "exocortex":
> I can definitely see that you want to decrease the I/O to tool use and I see this as kind of like an exocortex building on top of our neocortex. It's just the next layer and it just turns out to be in the cloud, but it is the next layer of the brain.

Ownership & Control vs Intelligence
> If it's like "not your weights, not your brain," that's interesting because a company is effectively controlling your exocortex and therefore part of it starts to feel kind of invasive. If this is my exocortex, I think people will care much more about ownership.

Models can be much smaller:
> I think it can be surprisingly small and I do think that the current models are wasting a ton of capacity remembering stuff that doesn't matter like they remember SHA hashes, they remember like the ancient. Because the data set is not curated the best. I think this will go away and we just need to get to the cognitive core. I think the cognitive core can be extremely small. It's just this thing that thinks and if it needs to look up information it knows how to use different tools. Is that like 3 billion parameters, is that 20 billion parameters? I think even 1 billion suffices. We'll probably get to that point and the models can be very small. I think the reason they can be very small is fundamentally I think distillation works surprisingly well.

> The internet data set, which is what we're working with, is like 0.001% cognition and 99.99% information, and most of it is not useful to the thinking part. Maybe there's no good way to represent that, so I think maybe a billion parameters gets you sort of like a good cognitive core. I think probably even 1 billion is too much.

Architecture of the Exocortex:
> It's very exciting given the question of on an edge device versus on the cloud, but also this raw cost of using the model. At less than a billion parameters I have my exocortex on a local device as well. It's probably not a single model.

> I do think you want to benefit from parallelization. You don't want to have a sequential process, you want to have a parallel process. I think companies to some extent are also kind of parallelization of work, but there's a hierarchy in a company because that's one way to have the information processing and the reductions that need to happen within the organization for information. So I think we'll probably end up with companies of LLMs.

> Models of different capabilities specialized to various unique domains: maybe there's a programmer, etc., and it will actually start to resemble companies to a very large extent. So you have the programmer and the program manager and similar kinds of roles of LLMs working in parallel, and coming together and orchestrating computation on your behalf.

> It's more like a swarm, you're like an ecosystem - it's like a biological ecosystem where you have specialized roles and niches. I think you'll start to resemble that; you have automatic escalation to other parts of the swarm depending on the difficulty of the problem and the CEO is a really brilliant cloud model but the workhorse can be a lot cheaper, maybe even open source models.

### Education

Why he cares about education:
> I'm always more interested in anything that kind of empowers people and I feel like I'm kind of on a high level like team human. I'm interested in things that AI can do to empower people and I don't want the future where people are kind of on the side of automation. I want people to be very in an empowered state and I want them to be amazing, even much more amazing than today.

The teacher is not the "front end" anymore:
> The teacher is kind of doing a lot of the course creation and the curriculum because currently, at current AI capability, I don't think the models are good enough to create a good course. But I think they're good to become the front end to the student and interpret the course to them. So basically, the teacher doesn't go to the people and the teacher is not the front end anymore. The teacher is on the back end designing the materials in the course and the AI is the front end.

We don't know the limits of human performance with better education:
> I think we haven't even scratched what's possible at all. So I think there's like two dimensions basically to it. Number one is the globalization dimension of like I want everyone to have really good education, but the other one is like how far can a single person go. I think both of those are very interesting and exciting.

Analogy-based learning:
> What's really helpful is if you're familiar with some other disciplines in the past, then it's really useful to make analogies to the things you know and that's extremely powerful in education.

In a pre AGI world, education is a tool, in a post AGI world, education is entertainment - like nobility of the Victorian era:
> I think in a pre-AGI society, education is useful and I think people will be motivated by that because they're climbing up the ladder economically. In a post-AGI society, we're just all society. I think education is entertainment to a much larger extent.

People are gonna keep returning to school as technology keeps changing:
> We have this antiquated concept of education where you go through school and then you graduate and go to work. Obviously, this will totally break down, especially in a society that's turning over so quickly that people are going to come back to school a lot more frequently as the technology changes very very quickly.

Useful subjects for a post-AGI world:
> I would say math, physics, CS kind of disciplines and the reason I say that is because I think it helps for just thinking skills. It's just like the best thinking skill core, that's my opinion. Of course I have a specific background, so I would think this, but that's just my view on it. I think like me taking physics classes and all these other classes just shaped the way I think and I think it's very useful for problem solving in general.

### Culture

Cultural aspects are the dominant variable in what people end up doing:
> I was in University of Toronto and Toronto, I don't think it's a very entrepreneurial environment. It doesn't even occur to you that you should be starting companies. I mean, it's not something that people are doing. You don't know friends who are doing it, you don't know that you're supposed to be looking up to it. People aren't reading books about all the founders and talking about them. It's just not a thing you aspire to or care about.