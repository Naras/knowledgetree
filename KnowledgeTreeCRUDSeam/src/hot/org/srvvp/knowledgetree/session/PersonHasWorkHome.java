package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personHasWorkHome")
public class PersonHasWorkHome extends EntityHome<PersonHasWork> {

	@In(create = true)
	PersonHome personHome;
	@In(create = true)
	PersonWorkRelationHome personWorkRelationHome;
	@In(create = true)
	WorkHome workHome;

	public void setPersonHasWorkId(PersonHasWorkId id) {
		setId(id);
	}

	public PersonHasWorkId getPersonHasWorkId() {
		return (PersonHasWorkId) getId();
	}

	public PersonHasWorkHome() {
		setPersonHasWorkId(new PersonHasWorkId());
	}

	@Override
	public boolean isIdDefined() {
		if (getPersonHasWorkId().getPerson() == null
				|| "".equals(getPersonHasWorkId().getPerson()))
			return false;
		if (getPersonHasWorkId().getRelation() == null
				|| "".equals(getPersonHasWorkId().getRelation()))
			return false;
		if (getPersonHasWorkId().getWork() == null
				|| "".equals(getPersonHasWorkId().getWork()))
			return false;
		return true;
	}

	@Override
	protected PersonHasWork createInstance() {
		PersonHasWork personHasWork = new PersonHasWork();
		personHasWork.setId(new PersonHasWorkId());
		return personHasWork;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Person person = personHome.getDefinedInstance();
		if (person != null) {
			getInstance().setPerson(person);
		}
		PersonWorkRelation personWorkRelation = personWorkRelationHome
				.getDefinedInstance();
		if (personWorkRelation != null) {
			getInstance().setPersonWorkRelation(personWorkRelation);
		}
		Work work = workHome.getDefinedInstance();
		if (work != null) {
			getInstance().setWork(work);
		}
	}

	public boolean isWired() {
		if (getInstance().getPerson() == null)
			return false;
		if (getInstance().getPersonWorkRelation() == null)
			return false;
		if (getInstance().getWork() == null)
			return false;
		return true;
	}

	public PersonHasWork getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
