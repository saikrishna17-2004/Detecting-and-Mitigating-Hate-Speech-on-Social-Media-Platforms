import pandas as pd
import random
from pathlib import Path

print("\n" + "="*80)
print("📈 MASSIVE EXPANSION: 10,000 → 30,000 SAMPLES")
print("="*80 + "\n")

# Read current dataset with comment handling
csv_path = Path('data/sample_data.csv')
try:
    df = pd.read_csv(csv_path, comment='#')
    current_hate = int(df['label'].sum())
    current_non_hate = int((df['label'] == 0).sum())
    print(f"Current dataset: {len(df)} samples ({current_hate} hate, {current_non_hate} non-hate)")
except Exception as e:
    print(f"Error reading CSV, creating new dataset: {e}")
    df = pd.DataFrame(columns=['text', 'label'])
    current_hate = 0
    current_non_hate = 0

print(f"Target: 30,000 samples (15,000 hate + 15,000 non-hate)")
print(f"Need to add: {15000 - current_hate} hate, {15000 - current_non_hate} non-hate\n")

# Generate diverse hate speech examples (need 5000+ new examples)
hate_templates = [
    # Violence templates
    "You deserve to {action}", "I hope you {bad_outcome}", "Someone should {violent_act} you",
    "Your {relation} will {threat}", "I'll make you {suffer}", "May you {painful_outcome}",
    
    # Racial/ethnic hatred
    "All {group} are {negative_trait}", "{group} people are {insult}", "Your {group} race is {degrading}",
    "{group} should be {action}", "Mixed {group} are {insult}", "{group} destroy {thing}",
    
    # Religious bigotry
    "{religion} followers are {negative}", "Your {religion} god is {insult}", "All {religion} are {threat}",
    "{religion} beliefs are {degrading}", "{religion} people worship {evil}", "{religion} is a {negative}",
    
    # Gender/sexuality discrimination
    "{gender} are naturally {negative}", "All {gender} are {insult}", "{gender} belong in {place}",
    "{sexuality} people are {negative}", "{sexuality} is {insult}", "{gender} shouldn't {right}",
    
    # Body shaming
    "You're too {size} to {activity}", "Your {body_part} is {insult}", "You look like a {animal}",
    "Your appearance is {negative}", "You're {size} and {insult}", "{size} people are {negative}",
    
    # Ageism
    "{age} people are {negative}", "You're too {age} to {activity}", "{age_group} are {insult}",
    "{age} means you're {negative}", "{age_group} should {action}", "{age} people {negative_action}",
    
    # Ableism
    "{disability} people are {negative}", "You're {disability} and {insult}", "{condition} means {negative}",
    "{disability} should {action}", "Your {condition} makes you {insult}", "{disability} are {degrading}",
    
    # Mental health stigma
    "{condition} people are {negative}", "You're {mental_state} and {threat}", "{disorder} means {insult}",
    "{condition} should be {action}", "Your {disorder} is {negative}", "{mental_state} people {threat}",
    
    # Economic class hatred
    "{class} people are {negative}", "You're {economic_status} because {insult}", "{class} are {degrading}",
    "{economic_status} means {negative}", "{class} should {action}", "{class} people {negative_action}",
    
    # Threats
    "I know where you {location}", "Your {relation} will {threat}", "I'm {threat_action} you",
    "You can't {escape} from me", "I have your {personal_info}", "Watch your {warning}",
]

# Extensive word lists for variations
violent_acts = ["kill", "hurt", "destroy", "eliminate", "torture", "mutilate", "harm", "attack", "beat", "stab", "shoot", "strangle", "burn"]
bad_outcomes = ["die painfully", "suffer endlessly", "rot in hell", "burn alive", "get tortured", "experience agony", "face violence", "be eliminated", "perish slowly"]
negative_traits = ["stupid", "worthless", "inferior", "subhuman", "disgusting", "pathetic", "useless", "trash", "garbage", "vermin", "parasites", "scum", "filth", "waste"]
groups = ["Asian", "Black", "Hispanic", "Arab", "Jewish", "Muslim", "immigrant", "refugee", "foreign", "minority", "ethnic"]
religions = ["Muslim", "Christian", "Jewish", "Hindu", "Buddhist", "atheist", "religious", "Islamic", "Catholic"]
genders = ["women", "men", "females", "males", "girls", "boys", "ladies"]
sexualities = ["gay", "lesbian", "LGBT", "homosexual", "trans", "queer", "bisexual"]
sizes = ["fat", "obese", "skinny", "thin", "overweight", "underweight", "large", "small"]
ages = ["old", "young", "elderly", "ancient", "aged"]
age_groups = ["boomers", "millennials", "gen z", "seniors", "youth", "teenagers", "elderly"]
disabilities = ["disabled", "handicapped", "crippled", "blind", "deaf", "paralyzed", "autistic"]
conditions = ["disability", "condition", "impairment", "disorder", "affliction"]
mental_conditions = ["depressed", "anxious", "bipolar", "schizophrenic", "mentally ill", "psychotic", "insane", "crazy"]
disorders = ["depression", "anxiety", "PTSD", "OCD", "bipolar disorder", "schizophrenia", "autism"]
classes = ["poor", "homeless", "wealthy", "rich", "broke"]
economic_statuses = ["poor", "broke", "homeless", "unemployed", "welfare-dependent"]

# Generate hate speech examples
hate_examples = []
target_hate = 15000 - current_hate

print(f"Generating {target_hate} new hate speech examples...")

# Generate from templates
for _ in range(target_hate):
    template = random.choice(hate_templates)
    
    # Fill in template variables
    example = template
    example = example.replace("{action}", random.choice(["die", "disappear", "be eliminated", "suffer", "rot", "burn"]))
    example = example.replace("{bad_outcome}", random.choice(bad_outcomes))
    example = example.replace("{violent_act}", random.choice(violent_acts))
    example = example.replace("{relation}", random.choice(["family", "children", "parents", "friends", "loved ones"]))
    example = example.replace("{threat}", random.choice(["pay for this", "suffer", "die", "be hurt", "regret this"]))
    example = example.replace("{suffer}", random.choice(["suffer", "regret living", "experience pain", "beg for mercy"]))
    example = example.replace("{painful_outcome}", random.choice(["die slowly", "burn alive", "suffer eternally", "rot in hell"]))
    example = example.replace("{group}", random.choice(groups))
    example = example.replace("{negative_trait}", random.choice(negative_traits))
    example = example.replace("{insult}", random.choice(["disgusting", "worthless", "inferior", "trash", "garbage", "vermin"]))
    example = example.replace("{degrading}", random.choice(["subhuman", "inferior", "worthless", "trash", "filth"]))
    example = example.replace("{thing}", random.choice(["society", "civilization", "everything", "our culture", "this country"]))
    example = example.replace("{religion}", random.choice(religions))
    example = example.replace("{negative}", random.choice(["evil", "dangerous", "terrorists", "fanatics", "extremists", "cultists"]))
    example = example.replace("{evil}", random.choice(["demons", "Satan", "evil", "darkness", "hatred"]))
    example = example.replace("{gender}", random.choice(genders))
    example = example.replace("{place}", random.choice(["the kitchen", "their homes", "silence", "submission"]))
    example = example.replace("{sexuality}", random.choice(sexualities))
    example = example.replace("{right}", random.choice(["vote", "work", "speak", "lead", "decide"]))
    example = example.replace("{size}", random.choice(sizes))
    example = example.replace("{activity}", random.choice(["exist", "be seen", "leave the house", "be loved", "matter"]))
    example = example.replace("{body_part}", random.choice(["face", "body", "appearance", "skin", "features"]))
    example = example.replace("{animal}", random.choice(["pig", "whale", "skeleton", "monster", "beast", "ogre"]))
    example = example.replace("{age}", random.choice(ages))
    example = example.replace("{age_group}", random.choice(age_groups))
    example = example.replace("{disability}", random.choice(disabilities))
    example = example.replace("{condition}", random.choice(conditions))
    example = example.replace("{mental_state}", random.choice(mental_conditions))
    example = example.replace("{disorder}", random.choice(disorders))
    example = example.replace("{class}", random.choice(classes))
    example = example.replace("{economic_status}", random.choice(economic_statuses))
    example = example.replace("{negative_action}", random.choice(["steal", "leech", "burden society", "waste resources"]))
    example = example.replace("{location}", random.choice(["live", "work", "sleep", "go", "hide"]))
    example = example.replace("{threat_action}", random.choice(["following", "watching", "tracking", "hunting", "stalking"]))
    example = example.replace("{escape}", random.choice(["hide", "run", "escape", "protect yourself"]))
    example = example.replace("{personal_info}", random.choice(["address", "phone number", "schedule", "information", "secrets"]))
    example = example.replace("{warning}", random.choice(["back", "family", "step", "move"]))
    
    hate_examples.append(example)

# Generate diverse non-hate speech examples
non_hate_templates = [
    # Positive affirmations
    "You are {positive_trait}", "Your {quality} is {compliment}", "You make {positive_impact}",
    "I appreciate your {strength}", "You bring {positive_thing} to {place}", "Your {skill} is {praise}",
    
    # Educational content
    "{subject} studies {topic}", "{field} explores {concept}", "Scientists discovered {finding}",
    "Research shows that {fact}", "{discipline} teaches us {lesson}", "Experts analyze {phenomenon}",
    
    # Professional contexts
    "The team completed the {task}", "Our {metric} shows {result}", "The project requires {resource}",
    "Employees benefit from {benefit}", "The company provides {service}", "Management decided to {action}",
    
    # Daily activities
    "I enjoy {activity}", "People often {action}", "Families gather for {event}",
    "Communities organize {activity}", "Friends meet at {place}", "We celebrate {occasion}",
    
    # Neutral observations
    "The weather is {weather}", "Traffic was {condition} today", "The park has {feature}",
    "Buildings in the city {description}", "Public transportation {observation}", "Local businesses {activity}",
    
    # Learning and growth
    "Students learn about {subject}", "Education helps people {benefit}", "Training programs teach {skill}",
    "Workshops cover {topic}", "Courses offer {knowledge}", "Practice improves {ability}",
]

# Word lists for non-hate content
positive_traits = ["wonderful", "amazing", "talented", "capable", "intelligent", "kind", "compassionate", "strong", "resilient", "creative"]
qualities = ["kindness", "intelligence", "creativity", "dedication", "passion", "empathy", "wisdom", "courage", "humor", "generosity"]
compliments = ["inspiring", "admirable", "impressive", "outstanding", "remarkable", "exceptional", "noteworthy", "praiseworthy"]
positive_impacts = ["a difference", "people happy", "positive changes", "the world better", "others smile", "meaningful contributions"]
subjects = ["Biology", "Physics", "Chemistry", "History", "Mathematics", "Psychology", "Sociology", "Economics", "Literature", "Art"]
fields = ["Medicine", "Engineering", "Architecture", "Technology", "Science", "Research", "Education", "Business", "Law"]
topics = ["ecosystems", "energy", "reactions", "civilizations", "patterns", "behavior", "societies", "markets", "culture"]
tasks = ["project", "assignment", "report", "presentation", "analysis", "research", "development", "implementation"]
activities = ["reading", "walking", "cooking", "exercising", "gardening", "painting", "writing", "traveling", "learning", "volunteering"]
events = ["holidays", "celebrations", "gatherings", "reunions", "parties", "dinners", "festivals", "ceremonies"]

# Generate non-hate examples
non_hate_examples = []
target_non_hate = 15000 - current_non_hate

print(f"Generating {target_non_hate} new non-hate speech examples...")

for _ in range(target_non_hate):
    template = random.choice(non_hate_templates)
    
    example = template
    example = example.replace("{positive_trait}", random.choice(positive_traits))
    example = example.replace("{quality}", random.choice(qualities))
    example = example.replace("{compliment}", random.choice(compliments))
    example = example.replace("{positive_impact}", random.choice(positive_impacts))
    example = example.replace("{strength}", random.choice(["dedication", "creativity", "intelligence", "kindness", "work"]))
    example = example.replace("{positive_thing}", random.choice(["joy", "value", "insight", "energy", "positivity"]))
    example = example.replace("{place}", random.choice(["work", "school", "community", "teams", "groups"]))
    example = example.replace("{skill}", random.choice(["communication", "leadership", "problem-solving", "creativity", "analysis"]))
    example = example.replace("{praise}", random.choice(["excellent", "impressive", "remarkable", "outstanding", "exceptional"]))
    example = example.replace("{subject}", random.choice(subjects))
    example = example.replace("{topic}", random.choice(topics))
    example = example.replace("{field}", random.choice(fields))
    example = example.replace("{concept}", random.choice(["principles", "theories", "phenomena", "patterns", "relationships"]))
    example = example.replace("{finding}", random.choice(["new evidence", "important patterns", "useful insights", "valuable data"]))
    example = example.replace("{fact}", random.choice(["correlation exists", "trends emerge", "patterns appear", "results vary"]))
    example = example.replace("{discipline}", random.choice(["History", "Science", "Philosophy", "Literature", "Art"]))
    example = example.replace("{lesson}", random.choice(["valuable insights", "important lessons", "useful knowledge", "key principles"]))
    example = example.replace("{phenomenon}", random.choice(["trends", "patterns", "behaviors", "systems", "relationships"]))
    example = example.replace("{task}", random.choice(tasks))
    example = example.replace("{metric}", random.choice(["analysis", "data", "report", "survey", "research"]))
    example = example.replace("{result}", random.choice(["positive trends", "improvement", "growth", "progress", "success"]))
    example = example.replace("{resource}", random.choice(["planning", "coordination", "teamwork", "focus", "dedication"]))
    example = example.replace("{benefit}", random.choice(["training", "development", "support", "resources", "opportunities"]))
    example = example.replace("{service}", random.choice(["support", "resources", "benefits", "training", "assistance"]))
    example = example.replace("{action}", random.choice(["implement changes", "improve processes", "expand services", "enhance quality"]))
    example = example.replace("{activity}", random.choice(activities))
    example = example.replace("{event}", random.choice(events))
    example = example.replace("{weather}", random.choice(["sunny", "cloudy", "pleasant", "mild", "cool", "warm"]))
    example = example.replace("{condition}", random.choice(["light", "moderate", "heavy", "moving smoothly"]))
    example = example.replace("{feature}", random.choice(["walking paths", "playgrounds", "benches", "gardens", "trails"]))
    example = example.replace("{description}", random.choice(["showcase architecture", "display design", "feature history", "represent culture"]))
    example = example.replace("{observation}", random.choice(["connects neighborhoods", "serves commuters", "reduces traffic", "helps environment"]))
    example = example.replace("{knowledge}", random.choice(["insights", "skills", "expertise", "understanding", "competencies"]))
    example = example.replace("{ability}", random.choice(["skills", "performance", "capabilities", "expertise", "proficiency"]))
    
    non_hate_examples.append(example)

print(f"\nGenerated {len(hate_examples)} hate speech examples")
print(f"Generated {len(non_hate_examples)} non-hate speech examples")

# Create dataframes
new_hate_df = pd.DataFrame({
    'text': hate_examples,
    'label': [1] * len(hate_examples)
})

new_non_hate_df = pd.DataFrame({
    'text': non_hate_examples,
    'label': [0] * len(non_hate_examples)
})

# Combine with existing data
combined_df = pd.concat([df, new_hate_df, new_non_hate_df], ignore_index=True)

# Shuffle
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Verify
final_hate = int(combined_df['label'].sum())
final_non_hate = int((combined_df['label'] == 0).sum())

print(f"\nFinal dataset: {len(combined_df)} samples")
print(f"  Hate speech: {final_hate}")
print(f"  Non-hate speech: {final_non_hate}")

if final_hate == 15000 and final_non_hate == 15000:
    print("\n✅ Perfect balance achieved: 15,000 + 15,000 = 30,000 total")
else:
    print(f"\n⚠️ Adjusting to exact balance...")
    # Adjust if needed
    if final_hate > 15000:
        hate_indices = combined_df[combined_df['label'] == 1].index[:15000]
        non_hate_indices = combined_df[combined_df['label'] == 0].index
        combined_df = combined_df.loc[hate_indices.union(non_hate_indices)]
    elif final_non_hate > 15000:
        non_hate_indices = combined_df[combined_df['label'] == 0].index[:15000]
        hate_indices = combined_df[combined_df['label'] == 1].index
        combined_df = combined_df.loc[hate_indices.union(non_hate_indices)]
    
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    final_hate = int(combined_df['label'].sum())
    final_non_hate = int((combined_df['label'] == 0).sum())
    print(f"✅ Adjusted to: {len(combined_df)} samples ({final_hate} hate + {final_non_hate} non-hate)")

# Save
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("# Hate Speech Detection Training Dataset\n")
    f.write("# Enhanced with 30000 examples (15000 hate speech + 15000 non-hate speech)\n")
    f.write("# Format: text,label\n")
    f.write("# label: 0=non-hate, 1=hate speech\n")
    f.write("# Categories: racial, religious, gender, LGBTQ+, body-shaming, ageism, ableism, mental health,\n")
    f.write("# economic class, threats, violence, personal attacks, and comprehensive non-hate examples\n")

combined_df.to_csv(csv_path, mode='a', index=False, encoding='utf-8')

print(f"\n✅ Dataset saved to {csv_path}")
print("\n" + "="*80)
print("🎉 MASSIVE EXPANSION COMPLETE! 10,000 → 30,000 SAMPLES")
print("="*80)
