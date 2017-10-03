package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personRelatestoPersonHome")
public class PersonRelatestoPersonHome
		extends
			EntityHome<PersonRelatestoPerson> {

	@In(create = true)
	PersonHome personHome;
	@In(create = true)
	PersonPersonRelationHome personPersonRelationHome;

	public void setPersonRelatestoPersonId(PersonRelatestoPersonId id) {
		setId(id);
	}

	public PersonRelatestoPersonId getPersonRelatestoPersonId() {
		return (PersonRelatestoPersonId) getId();
	}

	public PersonRelatestoPersonHome() {
		setPersonRelatestoPersonId(new PersonRelatestoPersonId());
	}

	@Override
	public boolean isIdDefined() {
		if (getPersonRelatestoPersonId().getPerson1() == null
				|| "".equals(getPersonRelatestoPersonId().getPerson1()))
			return false;
		if (getPersonRelatestoPersonId().getPerson2() == null
				|| "".equals(getPersonRelatestoPersonId().getPerson2()))
			return false;
		if (getPersonRelatestoPersonId().getRelation() == null
				|| "".equals(getPersonRelatestoPersonId().getRelation()))
			return false;
		return true;
	}

	@Override
	protected PersonRelatestoPerson createInstance() {
		PersonRelatestoPerson personRelatestoPerson = new PersonRelatestoPerson();
		personRelatestoPerson.setId(new PersonRelatestoPersonId());
		return personRelatestoPerson;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Person personByPerson1 = personHome.getDefinedInstance();
		if (personByPerson1 != null) {
			getInstance().setPersonByPerson1(personByPerson1);
		}
		Person personByPerson2 = personHome.getDefinedInstance();
		if (personByPerson2 != null) {
			getInstance().setPersonByPerson2(personByPerson2);
		}
		PersonPersonRelation personPersonRelation = personPersonRelationHome
				.getDefinedInstance();
		if (personPersonRelation != null) {
			getInstance().setPersonPersonRelation(personPersonRelation);
		}
	}

	public boolean isWired() {
		if (getInstance().getPersonByPerson1() == null)
			return false;
		if (getInstance().getPersonByPerson2() == null)
			return false;
		if (getInstance().getPersonPersonRelation() == null)
			return false;
		return true;
	}

	public PersonRelatestoPerson getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
