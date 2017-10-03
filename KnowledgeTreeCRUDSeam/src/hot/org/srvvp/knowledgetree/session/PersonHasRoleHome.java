package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personHasRoleHome")
public class PersonHasRoleHome extends EntityHome<PersonHasRole> {

	@In(create = true)
	PersonHome personHome;
	@In(create = true)
	RoleHome roleHome;

	public void setPersonHasRoleId(PersonHasRoleId id) {
		setId(id);
	}

	public PersonHasRoleId getPersonHasRoleId() {
		return (PersonHasRoleId) getId();
	}

	public PersonHasRoleHome() {
		setPersonHasRoleId(new PersonHasRoleId());
	}

	@Override
	public boolean isIdDefined() {
		if (getPersonHasRoleId().getPerson() == null
				|| "".equals(getPersonHasRoleId().getPerson()))
			return false;
		if (getPersonHasRoleId().getRole() == null
				|| "".equals(getPersonHasRoleId().getRole()))
			return false;
		return true;
	}

	@Override
	protected PersonHasRole createInstance() {
		PersonHasRole personHasRole = new PersonHasRole();
		personHasRole.setId(new PersonHasRoleId());
		return personHasRole;
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
		Role role = roleHome.getDefinedInstance();
		if (role != null) {
			getInstance().setRole(role);
		}
	}

	public boolean isWired() {
		if (getInstance().getPerson() == null)
			return false;
		if (getInstance().getRole() == null)
			return false;
		return true;
	}

	public PersonHasRole getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
