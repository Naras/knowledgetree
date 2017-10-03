package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personHome")
public class PersonHome extends EntityHome<Person> {

	@In(create = true)
	PersonlifeHome personlifeHome;

	public void setPersonId(String id) {
		setId(id);
	}

	public String getPersonId() {
		return (String) getId();
	}

	@Override
	protected Person createInstance() {
		Person person = new Person();
		return person;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Personlife personlife = personlifeHome.getDefinedInstance();
		if (personlife != null) {
			getInstance().setPersonlife(personlife);
		}
	}

	public boolean isWired() {
		return true;
	}

	public Person getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<Address> getAddresses() {
		return getInstance() == null ? null : new ArrayList<Address>(
				getInstance().getAddresses());
	}
	public List<PersonHasAffiliation> getPersonHasAffiliations() {
		return getInstance() == null
				? null
				: new ArrayList<PersonHasAffiliation>(getInstance()
						.getPersonHasAffiliations());
	}
	public List<PersonHasRole> getPersonHasRoles() {
		return getInstance() == null ? null : new ArrayList<PersonHasRole>(
				getInstance().getPersonHasRoles());
	}
	public List<PersonHasWork> getPersonHasWorks() {
		return getInstance() == null ? null : new ArrayList<PersonHasWork>(
				getInstance().getPersonHasWorks());
	}
	public List<PersonRelatestoPerson> getPersonRelatestoPersonsForPerson1() {
		return getInstance() == null
				? null
				: new ArrayList<PersonRelatestoPerson>(getInstance()
						.getPersonRelatestoPersonsForPerson1());
	}
	public List<PersonRelatestoPerson> getPersonRelatestoPersonsForPerson2() {
		return getInstance() == null
				? null
				: new ArrayList<PersonRelatestoPerson>(getInstance()
						.getPersonRelatestoPersonsForPerson2());
	}

}
