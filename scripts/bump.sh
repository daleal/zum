#!/bin/sh

if [ $(git symbolic-ref --short HEAD) != master ]; then
    echo "This script is supposed to be run on the \"master\" branch."
    exit 1
fi

if [ -z $1 ]; then
    echo "A bump rule (\"patch\", \"minor\", \"major\") must be passed as a parameter."
    exit 1
fi

# Get old version
OLD_VERSION=$(poetry version | rev | cut -d' ' -f1 | rev)

# Bump up pyproject version and get new version
poetry version $1 && NEW_VERSION=$(poetry version | rev | cut -d' ' -f1 | rev)

# Get the scripts directory name and the base directory name
SCRIPTS=$(cd $(dirname $0) && pwd)
BASEDIR=$(dirname $SCRIPTS)

# Get the metadata file
METADATA="$BASEDIR/zum/__init__.py"

# Get substitution strings
OLD_VERSION_SUBSTITUTION=$(echo $OLD_VERSION | sed "s/\./, /g")
NEW_VERSION_SUBSTITUTION=$(echo $NEW_VERSION | sed "s/\./, /g")

# Substitute the version in the python metadata file
sed -i.tmp "s#$OLD_VERSION_SUBSTITUTION#$NEW_VERSION_SUBSTITUTION#g" $METADATA && rm $METADATA.tmp

# Commit changes into release branch
git add $BASEDIR/pyproject.toml $BASEDIR/zum/__init__.py &&
git checkout -b release/prepare-$NEW_VERSION &&
git commit --message "Prepare $NEW_VERSION release"
