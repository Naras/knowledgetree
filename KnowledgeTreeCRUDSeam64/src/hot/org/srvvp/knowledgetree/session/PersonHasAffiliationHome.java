package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personHasAffiliationHome")
public class PersonHasAffiliationHome extends EntityHome<PersonHasAffiliation> {

	@In(create = true)
	AffiliationHome affiliationHome;
	@In(create = true)
	PersonHome personHome;

	public void setPersonHasAffiliationId(PersonHasAffiliationId id) {
		setId(id);
	}

	public PersonHasAffiliationId getPersonHasAffiliationId() {
		return (PersonHasAffiliationId) getId();
	}

	public PersonHasAffiliationHome() {
		setPersonHasAffiliationId(new PersonHasAffiliationId());
	}

	@Override
	public boolean isIdDefined() {
		if (getPersonHasAffiliationId().getAffiliation() == null
				|| "".equals(getPersonHasAffiliationId().getAffiliation()))
			return false;
		if (getPersonHasAffiliationId().getPerson() == null
				|| "".equals(getPersonHasAffiliationId().getPerson()))
			return false;
		return true;
	}

	@Override
	protected PersonHasAffiliation createInstance() {
		PersonHasAffiliation personHasAffiliation = new PersonHasAffiliation();
		personHasAffiliation.setId(new PersonHasAffiliationId());
		return personHasAffiliation;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Affiliation affiliation = affiliationHome.getDefinedInstance();
		if (affiliation != null) {
			getInstance().setAffiliation(affiliation);
		}
		Person person = personHome.getDefinedInstance();
		if (person != null) {
			getInstance().setPerson(person);
		}
	}

	public boolean isWired() {
		if (getInstance().getAffiliation() == null)
			return false;
		if (getInstance().getPerson() == null)
			return false;
		return true;
	}

	public PersonHasAffiliation getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
