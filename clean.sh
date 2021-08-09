!# /bin/bash

echo "Removing sqlite database"

rm -f db.sqlite3

echo "Removing udhari_user migrations and pycache"

rm -rf udhari_user/migrations
rm -rf udhari_user/__pycache__

echo "Removing udhari migrations and pycache"

rm -rf udhari/migrations
rm -rf udhari/__pycache__

echo "Removing expense migrations and pycache"

rm -rf expense/migrations
rm -rf expense/__pycache__

echo "Removing bills migrations and pycache"

rm -rf bill/migrations
rm -rf bill/__pycache__

echo "Removing trip migrations and pycache"

rm -rf trip/migrations
rm -rf trip/__pycache__

echo "Cleared project"

#==============================================#

echo "Creating fresh migrations"
python manage.py makemigrations udhari_user
echo "Successfully migrated udhari_user"
python manage.py makemigrations expense
echo "Successfully migrated expense"
python manage.py makemigrations udhari
echo "Successfully migrated udhari"
python manage.py makemigrations bill
echo "Successfully migrated bill"
python manage.py makemigrations trip
echo "Successfully migrated trip"

#==============================================#

echo "Migrating all changes ..."
python manage.py migrate

#==============================================#

echo "Creating superuser"
python manage.py createsuperuser --skip-checks





