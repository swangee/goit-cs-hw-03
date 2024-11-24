import faker
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import cmd
import os

client = MongoClient(
    f'mongodb+srv://goitmongo:{os.environ['CATS_MONGO_PWD']}@cluster0.4zlq0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
    server_api=ServerApi('1')
)

db = client.cats

def main():
    result_one = db.cats.insert_one(
        {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        }
    )

    print(result_one.inserted_id)

    result_many = db.cats.insert_many(
        [
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
        ]
    )
    print(result_many.inserted_ids)


class CatsCLI(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to CatsCLI. Type "help" for available commands.'

    def do_add_cats(self, line):
        """Adds cat with random nickname."""

        result_one = db.cats.insert_one(
            {
                "name": "Manny",
                "age": 7,
                "features": ["мявчить на двері", "табі", "гарно спить"],
            }
        )

        result_two = db.cats.insert_one(
            {
                "name": "Lucyk",
                "age": 1,
                "features": ["носиться шо дурний", "чорний", "трохи попахує"],
            }
        )

    def do_get_cat(self, name):
        print(db.cats.find_one({"name": name}))

    def do_get_cats(self, line):
        """Exit the CLI."""
        print(list(db.cats.find()))

    def do_set_age(self, line):
        name, age = line.split(' ')

        res = db.cats.update_one({"name": name}, {"$set": {"age": int(age)}})

        if res.matched_count == 0:
            print('failed to find a cat with the provided name')

            return

        print('age was updated', res)

    def do_add_feature(self, line):
        name, feature = line.split(' ')

        print(name, feature)

        res = db.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})

        if res.matched_count == 0:
            print('failed to find a cat with the provided name')

            return

        print('age was updated', res)

    def do_remove_cat(self, name):
        """Removes cat by its' name"""
        db.cats.delete_one({"name": name})
        print('Cat was removed')

    def do_remove_all_cats(self, name):
        """Removes all cats from the database"""
        db.cats.delete_many({})
        print('Cats where removed')

if __name__ == '__main__':
    CatsCLI().cmdloop()
